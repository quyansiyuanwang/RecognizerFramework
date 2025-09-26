# RecognizerFramework

![main language](https://img.shields.io/badge/python-3.13-blue?logo=python)
![platform](https://img.shields.io/badge/platform-windows-blueviolet.svg)
![license](https://img.shields.io/github/license/quyansiyuanwang/RecognizerFramework.svg)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/quyansiyuanwang/RecognizerFramework/checks.yml)
![main drive](https://img.shields.io/badge/drive-json-brightgreen.svg)
![repo size](https://img.shields.io/github/repo-size/quyansiyuanwang/RecognizerFramework)
![last commit](https://img.shields.io/github/last-commit/quyansiyuanwang/RecognizerFramework)
![doc last](https://img.shields.io/badge/docs%20last-2025--09--26-blue.svg)

RecognizerFramework is a modular workflow engine framework that supports defining automated task flows through JSON configuration files. It covers multiple task types including region recognition, input operations, system operations, and more, with excellent extensibility and maintainability.

---

## Documentation Language

[中文](./README.MD) | [English](./README.EN.MD)

---

## Features

- **Modular Design**: Core structures, controllers, and executors are layered for easy extension and maintenance.
- **Multi-Task Type Support**: Supports region recognition (ROI), OCR, input (keyboard/mouse), system operations, expression calculation (Calculate), and more.
- **JSON Configuration Driven**: Flexibly define task flows through JSON files, supporting advanced features like branching, dependencies, delays, and limits.
- **Background Input Support**: Supports sending input (text, keyboard, mouse) to specified windows without changing the current focus.
- **Intelligent Window Finding**: Supports finding windows by title, class name, or process name with both exact and fuzzy matching.
- **Log Management**: Multi-level log output (DEBUG/INFO/WARNING/ERROR/CRITICAL) with support for colored and file logging.
- **Type Safety**: Based on Pydantic type validation to ensure configuration and runtime safety.
- **Extensibility**: Supports custom executors, controllers, and exception types.

---

## Quick Start

### Environment Setup

1. Install dependencies:

   ```bash
   conda env create -f environment.yml
   conda activate RecognizerFramework
   ```

2. Or install with pip:

   ```bash
   pip install -r requirements.txt
   ```

### Run Example Workflow

1. Edit the `workflow/example.json` file to define the task flow.
2. Execute the following command to run the workflow:

   ```bash
   python main.py workflow/example.json
   ```

---

## JSON Configuration Guide

Workflows are defined through JSON files with the following main fields:

### Top-level Fields

- **begin**: Starting task name, must be a key in jobs.
- **globals**: Global configuration affecting all tasks.
  - debug: Whether to enable debug mode.
  - colorful: Whether to enable colored log output.
  - ignore: Whether to ignore errors.
  - logConfig: Log configuration (log level, file path, format, etc.).
- **jobs**: All task nodes, where the key is the task name and the value is the Job definition.

### Job Fields

- **type**: Task type (such as ROI, OCR, Input, System, Overload, Calculate, etc.).
- **description**: Task description.
- **before**: Pre-task configuration, supports tasks and ignore_errors.
- **after**: Post-task configuration, supports success, failure, always, and ignore_errors.
- **next**: Next task name or branch (supports success/failure branches).
- **delay**: Delay settings (pre, post).
- **limits**: Execution limits (maxCount, maxFailure, maxSuccess, exit).
- **needs**: Names of prerequisite tasks.
- Task type-related fields (such as roi, input, system, calculate, etc.) - see [JSON Field Usage Documentation](/docs/en-us/manual/JsonField.MD) for details.

---

## Example JSON

```json
{
  "$schema": "./schema/generated.schema.json",
  "begin": "StartTask",
  "globals": {
    "debug": true,
    "colorful": true,
    "logConfig": {
      "level": "INFO",
      "file": "log/example.log",
      "format": "%(levelname)s - %(asctime)s - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "jobs": {
    "StartTask": {
      "type": "Input",
      "description": "Start task",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "type": "Type",
          "keys": ["win", "r"],
          "duration": 0,
          "sep_time": 0
        }
      },
      "next": {
        "success": "BackgroundInputTask"
      },
      "delay": {
        "pre": 500,
        "post": 500
      }
    },
    "BackgroundInputTask": {
      "type": "Input",
      "description": "Background input example",
      "input": {
        "type": "Text",
        "background": true,
        "title": "Notepad",
        "text": {
          "message": "This is background input text that won't change the current focus",
          "duration": 1000
        }
      },
      "next": {
        "success": "EndTask"
      }
    },
    "EndTask": {
      "type": "System",
      "system": {
        "type": "Log",
        "log": {
          "message": "Process completed",
          "levels": ["INFO"]
        }
      },
      "description": "End task"
    }
  }
}
```

---

## Project Structure

This project adopts a modular design, divided into core code, script tools, documentation, configuration, and other parts for easy maintenance and extension. The following are descriptions of the main directories and files:

### Root Directory

- **main.py**: Project main entry point, starts the overall process.
- **environment.yml**: Conda environment dependency configuration for one-click development environment creation.
- **requirement.txt**: Pip dependency package list, suitable for pip environments.
- **test.py**: Test script for quick verification of main functionality.

### docs/ Documentation Directory

- **develop/Structure.MD**: Project structure description.
- **manual/JsonField.MD**: Detailed JSON configuration field description.

### script/ Scripts and Tools

- **\_\_main\_\_.py**: Script main entry point, supports `python -m script` to execute batch tools.
- **check_type.py**, **format.py**, **import_sort.py**, **schema.py**: Development auxiliary tools.
- **workflows.json**: Script workflow configuration example.
- **util/**: Common utility function modules (includes util.py).

### src/ Core Code

- **Models/**: Data model module, Pydantic-based type definitions and JSON parsing.
- **Typehints/**: Type hints and Pydantic type definitions.
- **Util/**: Common utility functions.
- **WorkflowEngine/**: Workflow engine (includes controllers, executors, exceptions, and other submodules).

### tests/ Test Directory

- **test_manager.py**, **\_\_init\_\_.py**, **executor/**, **workflow/**: Main test scripts and cases.

### tools/ Tools Directory

- **\_\_init\_\_.py**, **\_\_main\_\_.py**: Package initialization and main entry point.
- **GitCheckDiff/**: diff_only_docs.py and other tool scripts.
- **SingleScripts/**: all_commit.py, check_type.py, clean.py, export_env.py, format.py, import_sort.py, workflows.json.
- **util/**: util.py, \_\_init\_\_.py.

> Contains various development auxiliary tools such as scripts, plugins, etc.

### workflow/ Workflow Configuration

- Various workflow configuration files (\*.json) that define automation processes.
- **schema/**: JSON Schema folder.

---

## Contributing Guidelines

We welcome improvement suggestions or code contributions to this project! Please follow this process:

1. Fork this repository and create a branch.
2. Before submitting code, run:

   ```bash
   python -m script commit
   ```

   ```bash
   python -m tools all
   ```

3. Submit a Pull Request and describe your changes.

---

## Documentation

- **[JSON Field Description Documentation](/docs/en-us/manual/JsonField.MD)** - Detailed configuration field descriptions
- **[Project Structure Documentation](/docs/en-us/develop/Structure.MD)** - Project code structure descriptions

---

[![Contributors](https://contrib.rocks/image?repo=quyansiyuanwang/RecognizerFramework)](https://github.com/quyansiyuanwang/RecognizerFramework/graphs/contributors)

---

## Contact

If you have any questions or suggestions, please submit feedback through Issues.
