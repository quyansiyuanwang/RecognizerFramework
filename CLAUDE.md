# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Package manager:** `uv` (lockfile: `uv.lock`)

```bash
# Install all dependencies
uv sync

# Install deps via pip (used in CI — skips uv)
python deps/install_deps.py
python deps/install_mypy_types.py

# Run the application
python main.py <workflow.json>

# Run all tests
python -m unittest discover

# Run a single test file
python -m unittest tests/test_manager.py

# Run tests with verbose output (same as CI)
python -m unittest discover -s tests --verbose

# Type checking
python -m script check_type
python -m mypy src --ignore-missing-imports

# Format code (black + isort)
python -m script format

# Pre-commit checks (type check + format + sort imports)
python -m script commit

# Full CI-style build/check suite
python -m tools all

# Generate JSON schema from Pydantic models
python -m script schema

# Individual CI tool actions
python -m tools check_type     # mypy only
python -m tools format --check # black + isort check only
python -m tools clean          # remove __pycache__ dirs
```

## Architecture

RecognizerFramework is a **JSON-driven workflow automation engine for Windows**. A workflow is a JSON file describing a sequence of jobs; each job performs a typed task (screen recognition, OCR, keyboard/mouse input, system operations, expression evaluation). Results flow between jobs via the `use`/`returns` field.

### Execution pipeline

```
main.py
  → src/main.py::run(path)
    → CLI/cli.py          # argparse + interactive input fallback
    → WorkflowManager      # parse + validate JSON via Pydantic
    → ExecutorManager      # orchestrate execution with retry/branching
    → JobExecutor.dispatch()  # route to @register'd typed executor
```

### Key files

| Layer | File | Role |
|---|---|---|
| Entry | `main.py` | CLI entrypoint; parses workflow path, calls `run()` |
| CLI | `src/CLI/cli.py` | `argparse` with interactive fallback; calls `src/main.py::run()` |
| Facade | `src/main.py` | `execute_workflow()` creates `ExecutorManager` and runs it |
| Models | `src/Models/main.py` | Pydantic models: `Job`, `Workflow`, `Delay`, `Before`, `After`, `Next`, `Limits` |
| Globals | `src/Models/globals.py` | `Globals` / `LogConfig` — shared across all jobs |
| Sub-models | `src/Models/roi.py`, `input.py`, `system.py`, `calculate.py` | Per-type action definitions |
| Manager | `src/WorkflowEngine/manager.py` | `WorkflowManager` — JSON loading, job graph navigation, Overload resolution |
| Executor | `src/WorkflowEngine/executor.py` | `ExecutorManager` — execution loop, retry/limits, before/after hooks; `JobExecutor` — dispatches to typed executor via registry |
| Executors | `src/WorkflowEngine/Executors/*.py` | `@JobExecutor.register("Type")` — typed job implementations |
| Controllers | `src/WorkflowEngine/Controller/*.py` | Low-level system I/O (Win32 API, pyautogui, keyboard lib) |
| Type hints | `src/Typehints/structure.py` | `TaskReturnsDict[TV]`, `TaskAttemptDict` — the result/variable passing contract |

### Execution flow in detail

1. **`WorkflowManager`** loads the JSON, validates it against Pydantic, resolves `"Overload"` job inheritance (recursive merge with child-overrides-parent semantics), and provides job lookup / next-job navigation.

2. **`ExecutorManager`** runs the main execution loop:
   - Starts at `workflow.begin` job
   - For each job: checks `needs` dependencies, `limits` (maxCount/maxFailure/maxSuccess), runs `before` tasks → main job → `after` tasks
   - Follows `next` (string or `{success, failure}` dict) to determine next job
   - On `CriticalException`: checks `limits.exit` for a fallback job; if none, raises `CrashException` (hard abort)
   - On `IgnorableError`: logs warning, increments failure counter, continues
   - On `CrashException`: immediately terminates the entire workflow
   - `after` tasks support `success`, `failure`, and `always` conditional lists

3. **Variable flow**: job A sets `returns: { "x": "some_field" }`, job B references via `use: "A"`, making A's returned variables available in `self.use_vars`. The `use` variable is resolved by name lookup in the `ExecutorManager.task_vars` dict.

### The Controller layer (between executors and Win32)

Each executor delegates system interaction to a Controller. Controllers handle the safe execution pattern and foreground/background branching:

| Controller | Purpose |
|---|---|
| `InputController` | Mouse/keyboard/text input; foreground via `pyautogui`/`keyboard`, background via `win32gui.SendMessage` (WM_CHAR, WM_KEYDOWN, mouse messages) |
| `SystemController` | `sleep()` with live countdown logging, `run_command()` via subprocess |
| `CalculateController` | Expression evaluation (runtime math using job variables) |
| `LogController` | `LogManager` / `Logger` — leveled logging with color, file output, level filtering |

Controllers use `SafeRunner` (`Controller/Runner.py`) as a consistent error-handling wrapper that supports ignore-on-error, debug logging, and error callbacks.

### Typed executors (`src/WorkflowEngine/Executors/`)

Registered via `@JobExecutor.register("TypeName")`. Each must implement `Executor` (ABC with `execute(job, globals)`).

| Executor | Type | Input model | Actions |
|---|---|---|---|
| `ROIExecutor` | `"ROI"` | `ROI` | Screen capture, template matching (OpenCV), mouse move on match; supports window-anchored capture (with overlay/non-overlay modes) |
| `InputExecutor` | `"Input"` | `Input` | Text entry (foreground/background), mouse clicks/move/drag, keyboard press/release/type; window focus/injection |
| `OCRExecutor` | `"OCR"` | — | Stub — raises `NotImplementedError` |
| `SystemExecutor` | `"System"` | `System` | Command execution, clipboard paste, delay/sleep, logging |
| `CalculateExecutor` | `"Calculate"` | `Calculate` | Expression evaluation with variable substitution at runtime |

### Workflow JSON patterns

A workflow defines named jobs in a flat dictionary with explicit chaining:

```json
{
  "begin": "JOB-A",
  "jobs": {
    "JOB-A": { "type": "Calculate", "calculate": { ... }, "next": "JOB-B" },
    "JOB-B": { "type": "Input", "input": { ... }, "use": "JOB-A", "next": { "success": "END", "failure": "RETRY" } },
    "RETRY": { "type": "Input", "input": { ... } },
    "END": { "type": "System", "system": { "type": "Delay", "duration": 1000 } }
  }
}
```

Key fields: `type`, `next` (string or `{success, failure}`), `use` (pull variables from another job), `needs` (wait-for list), `before`/`after` (pre/post task hooks), `limits` (maxCount/maxFailure/maxSuccess/exit), `delay` (pre/post ms).

### Exception hierarchy (`src/WorkflowEngine/Exceptions/`)

```
ExecutionError (base — carries Optional[Job])
├── IgnorableError       # logged as warning; execution continues
│   ├── MatchingError, BeforeJobRunError, AfterJobRunError
│   └── MouseMovePositionError
├── CriticalException    # increments failure counter, may trigger limits.exit
│   ├── RetryError       # max attempts exceeded
│   └── (user-defined critical fates)
└── CrashException       # hard stop; aborts entire workflow
    ├── JobNotFoundError, JobTypeError, MissingRequiredError
    ├── NeededError, OverloadError, RecursiveError, WorkflowBeginError
    ├── ActionTypeError, DebugError, TemplateError, RegionError
    ├── WindowNotFoundError, MultipleMatchedError, IllegalWindowAreaError
    └── LogLevelError, CommandCrash
```

Project-specific exceptions live in `src/WorkflowEngine/Exceptions/execs/`, organized by domain (`roi.py`, `input.py`, `system.py`).

### Utility modules

| Module | Key contents |
|---|---|
| `src/WorkflowEngine/Util/window_util.py` | Window finding, focusing, enumeration via Win32 |
| `src/WorkflowEngine/Util/key_mapper.py` | Key name ↔ virtual key code mapping |
| `src/WorkflowEngine/Util/input_controller_util.py` | Clipboard get/set, lParam packing, VK lookup |
| `src/WorkflowEngine/Util/executor_works.py` | `delay()`, `update()` (set model attrs from kwargs), `get()` |
| `src/WorkflowEngine/Util/style.py` | ANSI color codes for log output |
| `src/Util/path_util.py` | Path resolution (current dir, absolute check) |

## Key Constraints

- **Windows-only**: depends on `win32gui`, `win32con`, `pywinauto`, `pyautogui`, `keyboard`, `comtypes`.
- **Python ≥ 3.12** required.
- CI (`.github/workflows/checks.yml`) enforces mypy strict typing, black formatting, and isort import ordering on every PR. Runs on `windows-latest` with Python 3.13. Skips type/style/tests if only `.md` files changed (diff check via `tools/GitCheckDiff/diff_only_docs.py`).
- Run `python -m script commit` before pushing to verify all checks.
- JSON schema for workflows is auto-generated from Pydantic models — regenerate with `python -m script schema` after model changes.
- Tests compare against `.json.answer` golden files in `tests/workflow/*/`.
- The `"Overload"` job type enables inheritance: a job can extend another job's definition, merging fields recursively (child values override parent, dicts merge deeply).
