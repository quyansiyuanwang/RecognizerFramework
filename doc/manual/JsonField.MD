# JSON 字段说明文档

## 目录

- [JSON 字段说明文档](#json-字段说明文档)
  - [目录](#目录)
  - [顶层字段](#顶层字段)
    - [`begin`](#begin)
    - [`globals`](#globals)
    - [`jobs`](#jobs)
  - [全局配置(globals)](#全局配置globals)
  - [任务定义(Job)](#任务定义job)
    - [通用字段-Job](#通用字段-job)
      - [type 可选值](#type-可选值)
    - [before 字段](#before-字段)
    - [ROI 任务](#roi-任务)
    - [Input 任务](#input-任务)
    - [System 任务](#system-任务)
  - [通用字段](#通用字段)
    - [delay](#delay)
    - [after](#after)
    - [limits](#limits)
  - [完整示例](#完整示例)

---

## 顶层字段

### `begin`

- **类型**：`string`
- **描述**：起始任务名，必须是 `jobs` 中的一个 key。

### `globals`

- **类型**：`object`
- **描述**：全局配置，影响所有任务。详见[全局配置](#全局配置globals)。

### `jobs`

- **类型**：`object`
- **描述**：所有任务节点，key 为任务名，value 为 Job 定义。

---

## 全局配置(globals)

| 字段名    | 类型    | 说明                                           |
| --------- | ------- | ---------------------------------------------- |
| debug     | boolean | 是否开启调试模式，输出详细日志。默认 `false`。 |
| colorful  | boolean | 是否彩色日志输出。默认 `true`。                |
| ignore    | boolean | 是否忽略错误。默认 `false`。                   |
| logConfig | object  | 日志配置，详见下表。                           |

**logConfig 子字段：**

| 字段名  | 类型    | 说明                                                                   |
| ------- | ------- | ---------------------------------------------------------------------- |
| level   | string  | 日志级别，可选：`LOG`、`DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` |
| file    | string  | 日志文件路径，若为 `null` 则不写入文件。                               |
| format  | string  | 日志格式化字符串，默认 `%(levelname)s - %(asctime)s - %(message)s`     |
| datefmt | string  | 日期时间格式化字符串，默认 `%Y-%m-%d %H:%M:%S.%f`                      |
| clear   | boolean | 是否清空日志，默认 `false`。                                           |

---

## 任务定义(Job)

### 通用字段-Job

| 字段名      | 类型          | 说明                                                                 |
| ----------- | ------------- | -------------------------------------------------------------------- |
| type        | string        | 任务类型，见下表。                                                   |
| description | string        | 任务描述，便于理解用途。                                             |
| before      | object        | 任务开始前的前置任务，包含 tasks 和 ignore_errors。                  |
| after       | object        | 任务完成后的后续任务，包含 success、failure、always、ignore_errors。 |
| next        | string/object | 下一个任务名或分支，支持 success/failure 分支。                      |
| delay       | object        | 延时设置，包含 pre、post。                                           |
| limits      | object        | 执行限制，包含 maxCount、maxFailure、maxSuccess、exit。              |
| needs       | array         | 依赖的前置任务名，全部完成后才会执行本任务。                         |

#### type 可选值

- `ROI`：区域识别
- `OCR`：文字识别（如有）
- `Input`：输入操作
- `System`：系统操作
- `Overload`：继承其他任务

---

### before 字段

| 字段名        | 类型    | 说明                 |
| ------------- | ------- | -------------------- |
| tasks         | array   | 前置任务名列表       |
| ignore_errors | boolean | 是否忽略错误         |

---

### ROI 任务

| 字段名   | 类型   | 说明                                                  |
| -------- | ------ | ----------------------------------------------------- |
| type     | string | 必填，`MoveMouse`（移动鼠标）、`DetectOnly`（仅检测） |
| image    | object | 必填，图片定义，见下表。                              |
| region   | object | 可选，识别区域，见下表。                              |
| window   | object | 可选，窗口捕获定义，支持窗口级区域识别。              |
| debug    | object | 可选，调试配置，支持调试和可视化 ROI。                |
| duration | int    | 可选，鼠标移动时间（毫秒）。                          |

**image 子字段：**

| 字段名     | 类型   | 说明         |
| ---------- | ------ | ------------ |
| path       | string | 图片文件路径 |
| confidence | float  | 识别置信度   |

**region 子字段：**

| 字段名 | 类型 | 说明        |
| ------ | ---- | ----------- |
| x      | int  | 区域 X 坐标 |
| y      | int  | 区域 Y 坐标 |
| width  | int  | 区域宽度    |
| height | int  | 区域高度    |

**window 子字段：**

| 字段名     | 类型   | 说明     |
| ---------- | ------ | -------- |
| title      | string | 窗口标题 |
| class_name | string | 窗口类名 |
| process    | string | 进程名称 |

**debug 子字段：**

| 字段名             | 类型 | 说明                     |
| ------------------ | ---- | ------------------------ |
| display_screenshot | bool | 是否显示截图，默认 False |

---

### Input 任务

| 字段名   | 类型   | 说明                                           |
| -------- | ------ | ---------------------------------------------- |
| type     | string | 必填，`Mouse`、`Keyboard`、`Text`              |
| mouse    | object | 可选，鼠标输入定义，仅 type 为 Mouse 时有效    |
| keyboard | object | 可选，键盘输入定义，仅 type 为 Keyboard 时有效 |
| text     | object | 可选，文本输入定义，仅 type 为 Text 时有效     |

**mouse 子字段：**

| 字段名   | 类型   | 说明                                           |
| -------- | ------ | ---------------------------------------------- |
| type     | string | `LClick`、`RClick`、`MClick`、`Move`、`MoveTo` |
| x        | int    | X 坐标                                         |
| y        | int    | Y 坐标                                         |
| duration | int    | 延时（毫秒）                                   |

**keyboard 子字段：**

| 字段名   | 类型  | 说明                         |
| -------- | ----- | ---------------------------- |
| keys     | array | 按键列表，如 `["ctrl", "v"]` |
| duration | int   | 按下到释放的时间（毫秒）     |
| sep_time | int   | 按键间隔时间（毫秒）         |

**text 子字段：**

| 字段名   | 类型   | 说明                 |
| -------- | ------ | -------------------- |
| text     | string | 要输入的文本         |
| duration | int    | 文本输入时间（毫秒） |

---

### System 任务

| 字段名   | 类型   | 说明                                                  |
| -------- | ------ | ----------------------------------------------------- |
| type     | string | 必填，`Delay`（延时）、`Paste`（粘贴）、`Log`（日志） |
| duration | int    | 可选，延时操作定义，仅 type 为 Delay 时有效           |
| log      | object | 可选，日志记录定义，仅 type 为 Log 时有效             |

**log 子字段：**

| 字段名  | 类型   | 说明                                                                       |
| ------- | ------ | -------------------------------------------------------------------------- |
| message | string | 日志消息，必填                                                             |
| levels  | array  | 日志级别列表，可选：`LOG`、`DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` |

---

## 通用字段

### delay

| 字段名 | 类型 | 说明             |
| ------ | ---- | ---------------- |
| pre    | int  | 前置延时（毫秒） |
| post   | int  | 后置延时（毫秒） |

### after

| 字段名        | 类型    | 说明                 |
| ------------- | ------- | -------------------- |
| success       | array   | 成功时的任务名列表   |
| failure       | array   | 失败时的任务名列表   |
| always        | array   | 总是执行的任务名列表 |
| ignore_errors | boolean | 是否忽略错误         |

### limits

| 字段名     | 类型   | 说明                         |
| ---------- | ------ | ---------------------------- |
| maxCount   | int    | 最大执行次数，默认 -1 不限制 |
| maxFailure | int    | 最大失败次数，默认 -1 不限制 |
| maxSuccess | int    | 最大成功次数，默认 -1 不限制 |
| exit       | string | 达到最大次数后切换的任务名   |

---

## 完整示例

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
      "description": "启动任务",
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
          "message": "流程结束",
          "levels": ["INFO"]
        }
      },
      "description": "结束任务"
    }
  }
}
```

---

如需详细字段说明，请查阅 `src/Models` 目录下各模型定义，或以 `workflow/schema/generated.schema.json` 为准。若有疑问请联系开发者。
