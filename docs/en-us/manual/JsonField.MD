# JSON Field Documentation

## Table of Contents

- [JSON Field Documentation](#json-field-documentation)
  - [Table of Contents](#table-of-contents)
  - [Top-level Fields](#top-level-fields)
    - [`begin`](#begin)
    - [`globals`](#globals)
    - [`jobs`](#jobs)
  - [Global Configuration (globals)](#global-configuration-globals)
  - [Task Definition (Job)](#task-definition-job)
    - [Common Job Fields](#common-job-fields)
      - [type Options](#type-options)
    - [before Field](#before-field)
    - [ROI Task](#roi-task)
    - [Input Task](#input-task)
    - [System Task](#system-task)
    - [Calculate Task](#calculate-task)
  - [Common Fields](#common-fields)
    - [delay](#delay)
    - [after](#after)
    - [limits](#limits)
  - [Complete Example](#complete-example)

---

## Top-level Fields

### `begin`

- **Type**: `string`
- **Description**: Starting task name, must be a key in `jobs`.

### `globals`

- **Type**: `object`
- **Description**: Global configuration affecting all tasks. See [Global Configuration](#global-configuration-globals) for details.

### `jobs`

- **Type**: `object`
- **Description**: All task nodes, where the key is the task name and the value is the Job definition.

---

## Global Configuration (globals)

| Field Name | Type    | Description                                                   |
| ---------- | ------- | ------------------------------------------------------------- |
| debug      | boolean | Whether to enable debug mode for detailed logging. Default `false`. |
| colorful   | boolean | Whether to enable colored log output. Default `true`.        |
| ignore     | boolean | Whether to ignore errors. Default `false`.                   |
| logConfig  | object  | Log configuration, see table below.                          |

**logConfig sub-fields:**

| Field Name | Type    | Description                                                                         |
| ---------- | ------- | ----------------------------------------------------------------------------------- |
| level      | string  | Log level, options: `LOG`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`        |
| file       | string  | Log file path, if `null` then no file output.                                     |
| format     | string  | Log format string, default `%(levelname)s - %(asctime)s - %(message)s`           |
| datefmt    | string  | Date time format string, default `%Y-%m-%d %H:%M:%S.%f`                          |
| clear      | boolean | Whether to clear log file, default `false`.                                       |

---

## Task Definition (Job)

### Common Job Fields

| Field Name  | Type          | Description                                                                          |
| ----------- | ------------- | ------------------------------------------------------------------------------------ |
| type        | string        | Task type, see table below.                                                         |
| description | string        | Task description for understanding purpose.                                          |
| before      | object        | Pre-tasks before task execution, includes tasks and ignore_errors.                  |
| after       | object        | Post-tasks after task completion, includes success, failure, always, ignore_errors. |
| next        | string/object | Next task name or branch, supports success/failure branches.                        |
| delay       | object        | Delay settings, includes pre, post.                                                 |
| limits      | object        | Execution limits, includes maxCount, maxFailure, maxSuccess, exit.                  |
| needs       | array         | Names of prerequisite tasks, this task executes only after all are completed.       |
| calculate   | object/null   | Calculate task definition, only valid when type is Calculate.                       |

#### type Options

- `ROI`: Region recognition
- `OCR`: Text recognition (if available)
- `Input`: Input operations
- `System`: System operations
- `Overload`: Inherit from other tasks
- `Calculate`: Expression calculation task

---

### before Field

| Field Name    | Type    | Description                    |
| ------------- | ------- | ------------------------------ |
| tasks         | array   | List of pre-task names         |
| ignore_errors | boolean | Whether to ignore errors       |

---

### ROI Task

| Field Name | Type   | Description                                                      |
| ---------- | ------ | ---------------------------------------------------------------- |
| type       | string | Required, `MoveMouse` (move mouse), `DetectOnly` (detect only)   |
| image      | object | Required, image definition, see table below.                     |
| region     | object | Optional, recognition region, see table below.                   |
| window     | object | Optional, window capture definition for window-level region recognition. |
| debug      | object | Optional, debug configuration for ROI debugging and visualization. |
| duration   | int    | Optional, mouse movement duration (milliseconds).                |

**image sub-fields:**

| Field Name | Type   | Description           |
| ---------- | ------ | --------------------- |
| path       | string | Image file path       |
| confidence | float  | Recognition confidence |

**region sub-fields:**

| Field Name | Type | Description      |
| ---------- | ---- | ---------------- |
| x          | int  | Region X coordinate |
| y          | int  | Region Y coordinate |
| width      | int  | Region width     |
| height     | int  | Region height    |

**window sub-fields:**

| Field Name | Type   | Description      |
| ---------- | ------ | ---------------- |
| title      | string | Window title     |
| class_name | string | Window class name |
| process    | string | Process name     |

**debug sub-fields:**

| Field Name         | Type | Description                              |
| ------------------ | ---- | ---------------------------------------- |
| display_screenshot | bool | Whether to display screenshot, default False |

---

### Input Task

| Field Name   | Type    | Description                                                    |
| ------------ | ------- | -------------------------------------------------------------- |
| type         | string  | Required, `Mouse`, `Keyboard`, `Text`                          |
| mouse        | object  | Optional, mouse input definition, only valid when type is Mouse |
| keyboard     | object  | Optional, keyboard input definition, only valid when type is Keyboard |
| text         | object  | Optional, text input definition, only valid when type is Text  |
| background   | boolean | Optional, whether to execute in background, default false     |
| focus        | boolean | Optional, whether to switch window focus before execution, default false |
| title        | string  | Optional, target window title for window finding              |
| class_name   | string  | Optional, target window class name for window finding         |
| process      | string  | Optional, target process name for window finding              |
| visible_only | boolean | Optional, whether to find only visible windows, default true  |
| exact_match  | boolean | Optional, whether to use exact window matching, default false |

**Background Input Feature Description:**

- When `background` is true, enables background input mode without changing current focus window
- When `focus` is true, brings target window to foreground before executing input
- Window finding fields (title, class_name, process) require at least one to be provided
- `exact_match` controls whether to use exact matching (true) or contains matching (false)
- For detailed usage, please refer to [Background Input Feature Guide](BackgroundInput.MD)

**mouse sub-fields:**

| Field Name | Type   | Description                                    |
| ---------- | ------ | ---------------------------------------------- |
| type       | string | `LClick`, `RClick`, `MClick`, `Move`, `MoveTo` |
| x          | int    | X coordinate                                   |
| y          | int    | Y coordinate                                   |
| duration   | int    | Delay (milliseconds)                           |

**keyboard sub-fields:**

| Field Name | Type  | Description                               |
| ---------- | ----- | ----------------------------------------- |
| keys       | array | Key list, e.g., `["ctrl", "v"]`          |
| duration   | int   | Time from press to release (milliseconds) |
| sep_time   | int   | Interval between keys (milliseconds)      |

**text sub-fields:**

| Field Name | Type   | Description                      |
| ---------- | ------ | -------------------------------- |
| text       | string | Text to input                    |
| duration   | int    | Text input duration (milliseconds) |

---

### System Task

| Field Name | Type   | Description                                              |
| ---------- | ------ | -------------------------------------------------------- |
| type       | string | Required, `Delay` (delay), `Paste` (paste), `Log` (log) |
| duration   | int    | Optional, delay operation definition, only valid when type is Delay |
| log        | object | Optional, log record definition, only valid when type is Log |

**log sub-fields:**

| Field Name | Type   | Description                                                              |
| ---------- | ------ | ------------------------------------------------------------------------ |
| message    | string | Log message, required                                                    |
| levels     | array  | Log level list, options: `LOG`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

---

### Calculate Task

| Field Name  | Type   | Description                                                                                    |
| ----------- | ------ | ---------------------------------------------------------------------------------------------- |
| expressions | object | Dictionary of calculation expressions, key is variable name, value is expression string or number. Expressions can reference other variables. |
| variables   | object | Variables used in calculation and their initial values (optional).                            |
| returns     | object | Variable name mapping for calculation results, key is new variable name, value is expression variable name (optional). |

**Expression Support:**

- Supports addition `+`, subtraction `-`, multiplication `*`, division `/`, power `**`, integer division `//`, modulo `%`.
- Supports math functions starting with `$`, such as `$sqrt(a)`, `$pow(b,2)`.
- Expressions can nest references to other variables.

**Example:**

```json
{
  "type": "Calculate",
  "calculate": {
    "expressions": {
      "a": "b * b - c",
      "b": "$sqrt(x) + 1",
      "c": 2
    },
    "variables": {
      "x": 9
    },
    "returns": {
      "result": "a"
    }
  },
  "description": "Calculate expression task"
}
```

---

## Common Fields

### delay

| Field Name | Type | Description                   |
| ---------- | ---- | ----------------------------- |
| pre        | int  | Pre-delay (milliseconds)      |
| post       | int  | Post-delay (milliseconds)     |

### after

| Field Name    | Type    | Description                   |
| ------------- | ------- | ----------------------------- |
| success       | array   | Task name list for success   |
| failure       | array   | Task name list for failure   |
| always        | array   | Task name list always executed |
| ignore_errors | boolean | Whether to ignore errors      |

### limits

| Field Name | Type   | Description                                   |
| ---------- | ------ | --------------------------------------------- |
| maxCount   | int    | Maximum execution count, default -1 unlimited |
| maxFailure | int    | Maximum failure count, default -1 unlimited   |
| maxSuccess | int    | Maximum success count, default -1 unlimited   |
| exit       | string | Task name to switch to after reaching maximum |

---

## Complete Example

```json
{
  "$schema": "./schema/schema.json",
  "begin": "StartTask",
  "globals": {
    "debug": true,
    "colorful": true,
    "ignore": false,
    "logConfig": {
      "level": "INFO",
      "file": "log/example.log",
      "format": "%(levelname)s - %(asctime)s - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S.%f"
    }
  },
  "jobs": {
    "StartTask": {
      "type": "Input",
      "description": "Start task",
      "input": {
        "type": "Keyboard",
        "keyboard": {
          "keys": ["win", "r"],
          "duration": 0,
          "sep_time": 0
        }
      },
      "next": {
        "success": "EndTask"
      },
      "delay": {
        "pre": 500,
        "post": 500
      },
      "limits": {
        "maxCount": 3
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

For detailed field descriptions, please refer to the model definitions in the `src/Models` directory, or use `workflow/schema/generated.schema.json` as reference. If you have any questions, please contact the developers.