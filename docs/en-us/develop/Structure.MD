# Project Structure Documentation

This project adopts a modular design, divided into core code, script tools, documentation, configuration, and other parts for easy maintenance and extension. The following is the latest detailed directory and file description:

## Root Directory

- **main.py**: Project main entry point, starts the overall process.
- **environment.yml**: Conda environment dependency configuration for one-click development environment creation.
- **requirement.txt**: Pip dependency package list, suitable for pip environments.
- **test.py**: Test script for quick verification of main functionality.

## docs/ Documentation Directory

- **develop/Structure.MD**: Project structure description (this file).
- **manual/JsonField.MD**: Detailed JSON configuration field description, including all available fields, types, and examples.

## script/ Scripts and Tools

- **\_\_main\_\_.py**: Script main entry point, supports `python -m script` to execute batch tools (with improved type annotations).
- **check_type.py**: Type checking tool to assist with type safety during development.
- **format.py**: Code formatting tool for unified code style.
- **import_sort.py**: Import sorting tool that automatically organizes import order.
- **schema.py**: JSON Schema related scripts for automatic schema generation/validation.
- **workflows.json**: Script workflow configuration example.
- **util/**: Common utility function modules.
  - **util.py**: Collection of commonly used utility functions.

## src/ Core Code

- **Models/**: Data model module, Pydantic-based type definitions and JSON parsing.

  - **globals.py**: Global configuration model.
  - **input.py**: Input task model.
  - **main.py**: Workflow model, including core definitions like `Workflow`, `Job`, etc.
  - **roi.py**: Region recognition task model.
  - **system.py**: System task model.

- **Typehints/**: Type hints and Pydantic type definitions.

  - **basic.py**: Basic type definitions.
  - **roi.py**: ROI type definitions.
  - **structure.py**: Structure-related type definitions.

- **Util/**: Common utility functions.

  - **path_util.py**: Path-related utility functions.
  - **util.py**: Collection of commonly used utility functions.

- **WorkflowEngine/**: Workflow engine.
  - **executor.py**: Executor base class and registration logic (with exception handling and cache optimization).
  - **manager.py**: Workflow manager responsible for task scheduling and state management (with exception handling optimization).
  - **Controller/**: Controller submodules.
    - **InputController.py**: Input controller that encapsulates mouse/keyboard operations.
    - **LogController.py**: Log management for unified log output.
    - **Runner.py**: Workflow runner that schedules tasks.
    - **SystemController.py**: System controller that handles system-level tasks.
  - **Exceptions/**: Custom exception definitions.
    - **base.py**: Base exception types.
    - **crash.py**: General crash exceptions.
    - **critical.py**: Critical exception types.
    - **ignorable.py**: Ignorable exception types.
    - **execs/**: Subdivided execution exceptions.
      - **input.py**: Input-related exceptions.
      - **roi.py**: ROI-related exceptions.
      - **roi_crash.py**: ROI crash exceptions.
      - **system.py**: System-related exceptions.
      - **system_crash.py**: System crash exceptions.
  - **Executors/**: Executor modules.
    - **InputExecutor.py**: Input task executor.
    - **OCRExecutor.py**: OCR task executor.
    - **ROIExecutor.py**: Region recognition task executor (supports window capture and debugging).
    - **SystemExecutor.py**: System task executor.
  - **Util/**: Engine-related utilities.
    - **executor_works.py**: Executor workflow tools.
    - **style.py**: Style tools.
    - **util.py**: Engine common utilities.

## tests/ Test Directory

- **test_manager.py**: Main test script.
- **\_\_init\_\_.py**: Package initialization.
- **executor/**: Reserved for executor-related tests (currently empty).
- **workflow/**: Workflow-related test cases.
  - **`year`-`month`-`day`T`hour`.`minute`/**: Test sets grouped by time.
    - **\*.json**: Test inputs.
    - **\*.answer**: Expected outputs.

## tools/ Tools Directory

- **\_\_init\_\_.py**, **\_\_main\_\_.py**: Package initialization and main entry point.
- **GitCheckDiff/**
  - **diff_only_docs.py**: Tool script that only detects .md file changes.
- **SingleScripts/**
  - **all_commit.py**: Commit history related tools.
  - **check_type.py**: Type checking script.
  - **clean.py**: Clean cache, temporary files, etc.
  - **export_env.py**: Export environment dependencies.
  - **format.py**: Code formatting script.
  - **import_sort.py**: Import sorting script.
  - **workflows.json**: Tool workflow configuration.
- **util/**
  - **util.py**: Utility function implementations.
  - **\_\_init\_\_.py**: util package initialization.

> Contains various development auxiliary tools such as scripts, plugins, etc.

## workflow/ Workflow Configuration

- Various workflow configuration files (\*.json) that define automation processes.
- **schema/**: JSON Schema folder.
  - **generated.schema.json**: Schema file automatically generated from Pydantic types.
- **tests/**: Workflow-related test cases.

---

> Each module has clear responsibilities, making it easy to extend and maintain. Developers are recommended to first review `src/` and `doc/manual/JsonField.MD` to understand the core logic and configuration methods.