# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Package manager:** `uv` (lockfile: `uv.lock`)

```bash
# Install dependencies
uv sync

# Run the application
python main.py <workflow.json>

# Run all tests
python -m unittest discover

# Run a single test file
python -m unittest tests/test_manager.py

# Type checking
python -m script check_type
# or directly:
python -m mypy src --ignore-missing-imports

# Format code (black + isort)
python -m script format

# Pre-commit checks (type check + format + sort imports)
python -m script commit

# Full build/check suite
python -m tools all

# Generate JSON schema from Pydantic models
python -m script schema
```

## Architecture

RecognizerFramework is a JSON-driven workflow automation engine for Windows. A workflow is a JSON file describing a sequence of jobs; each job performs a typed task (screen recognition, OCR, keyboard/mouse input, system operations, expression evaluation).

### Execution pipeline

```
main.py → src/CLI/cli.py
       → WorkflowManager (manager.py)   # parse + validate JSON via Pydantic
       → ExecutorManager (executor.py)  # orchestrate job execution
       → JobExecutor.dispatch()         # route to registered typed executor
```

1. **`WorkflowManager`** (`src/WorkflowEngine/manager.py`): Loads a JSON workflow, validates it against Pydantic models, resolves "Overload" job inheritance, and builds a flat job map.
2. **`ExecutorManager`** (`src/WorkflowEngine/executor.py`): Iterates the job graph following `next`/`needs` chains, applies `before`/`after`/`always` task sequences, enforces execution limits (`maxCount`, `maxFailure`, `maxSuccess`), and passes results between jobs via the `use` field.
3. **`JobExecutor`** dispatches each job to a registered executor by type name. New task types are registered with `@JobExecutor.register("TypeName")`.

### Typed executors (`src/WorkflowEngine/Executors/`)

| File | Handles |
|---|---|
| `ROIExecutor.py` | Screen capture, template matching, mouse movement to region |
| `InputExecutor.py` | Keyboard / mouse / text input (supports background window injection) |
| `OCRExecutor.py` | OCR on screen regions |
| `SystemExecutor.py` | Logging, delays, system-level operations |

### Data models (`src/Models/`)

All JSON-sourced data is validated by Pydantic models. Key models:
- `main.py` — `Job`, `Workflow`, `Delay`, `Before`, `After`, `Next`, `Limits`
- `roi.py` — `ROI`, `ROI_Image`, `ROI_Region`, `ROI_Window`
- `input.py` — `Input_Mouse`, `Input_Keyboard`, `Input_Text`
- `globals.py` — global configuration

### Exception hierarchy (`src/WorkflowEngine/Exceptions/`)

- `CrashException` — hard stop, abort the entire workflow
- `CriticalException` — triggers retry/failure branching logic
- `IgnorableError` — warning only, execution continues

### Variable passing between jobs

Each job execution returns a `TaskReturnsDict` (`src/Typehints/structure.py`) containing `returns`, `variables`, and `result`. Downstream jobs consume these via the `use` field in their JSON definition.

## Key constraints

- **Windows-only**: depends on `win32gui`, `win32con`, `pywinauto`, `pyautogui`, `keyboard`, `comtypes`.
- **Python ≥ 3.12** required.
- CI enforces mypy strict typing, black formatting, and isort import ordering on every PR. Run `python -m script commit` before pushing.
- JSON schema for workflows is auto-generated from the Pydantic models — regenerate with `python -m script schema` after model changes.
