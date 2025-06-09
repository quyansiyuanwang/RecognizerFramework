# JSON 字段使用文档

## 目录

- [JSON 字段使用文档](#json-字段使用文档)
  - [目录](#目录)
  - [顶层字段](#顶层字段)
    - [`begin`](#begin)
    - [`globals`](#globals)
  - [`Job` 字段](#job-字段)
    - [`type`](#type)
    - [`action`](#action)
    - [`description`](#description)
    - [`image`](#image)
    - [`region`](#region)
    - [`next`](#next)
    - [`delay`](#delay)
    - [`needs`](#needs)
    - [`limits`](#limits)
  - [示例 JSON](#示例-json)

## 顶层字段

### `begin`

- **类型**: `string`
- **描述**: 起始任务名，必须是 `jobs` 中的一个 key。

### `globals`

- **类型**: `object`
- **描述**: 全局配置，影响所有任务。

- **子字段**:
  - `debug`: `boolean` - 是否开启调试模式，输出详细日志。
  - `colorful`: `boolean` - 是否启用彩色日志输出。
  - `ignore`: `boolean` - 是否忽略错误。
  - `logConfig`: `object` - 日志配置。
    - `level`: `string` - 日志级别，可选值：`DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL`。
    - `file`: `string` - 日志文件路径，若为 `null` 则不写入文件。
    - `format`: `string` - 日志格式化字符串，默认值：`"%(levelname)s - %(asctime)s - %(message)s"`。
    - `datefmt`: `string` - 日期时间格式化字符串，默认值：`"%Y-%m-%d %H:%M:%S.%f"`。

## `Job` 字段

### `type`

- **类型**: `string`
- **描述**: 任务类型，可选值：
  - `ROI`: 区域识别
  - `OCR`: 文字识别
  - `Input`: 输入操作
  - `System`: 系统操作

### `action`

- **类型**: 可选对象
- **描述**: 定义任务的具体动作，取决于任务类型。

- **子字段**:
  - `type`: 字符串，必填。可选值包括：`"LClick"`、`"RClick"`、`"DoubleClick"`、`"TextInput"`、`"KeyboardInput"`、`"Delay"`、`"Paste"`、`"Typewrite"`、`"Hotkey"`。
  - `position`: 对象，可选。定义点击或操作的位置。
  - `keys`: 数组，可选。键盘输入的按键列表，例如：`["ctrl", "c"]`。
  - `text`: 字符串，可选。要输入的文本，例如：`"Hello World"`。
  - `duration`: 整数，可选。操作持续时间或延时，单位为毫秒，例如：`1000`。
  - `use_keyboard`: 布尔值，可选。是否使用键盘输入，例如：`true`。

### `description`

- **类型**: 字符串，可选
- **描述**: 任务的描述信息，用于说明任务的用途。

### `image`

- **类型**: `object`
- **描述**: 图片信息（ROI/OCR 专用），包含路径和置信度。

### `region`

- **类型**: `object`
- **描述**: 操作区域，指定任务作用的屏幕区域。

### `next`

- **类型**: `string | object`
- **描述**: 下一个任务名或分支，支持 `success`/`failure` 分支。

### `delay`

- **类型**: `object`
- **描述**: 延时设置，控制任务前中后等待时间。

- **子字段**:
  - `pre`: `integer` - 前置延时（毫秒）。
  - `cur`: `integer` - 当前任务延时（毫秒）。
  - `post`: `integer` - 后置延时（毫秒）。

### `needs`

- **类型**: `array`
- **描述**: 依赖的前置任务名，只有全部完成后才会执行本任务。

### `limits`

- **类型**: `object`
- **描述**: 任务执行限制。

- **子字段**:
  - `maxCount`: `integer` - 最大执行次数，默认值：`-1`（不限制）。
  - `maxFailure`: `integer` - 最大失败次数，默认值：`-1`（不限制）。
  - `maxSuccess`: `integer` - 最大成功次数，默认值：`-1`（不限制）。

## 示例 JSON

```json
{
  "$schema": "./schema/schema.json",
  "begin": "StartTask",
  "globals": {
    "debug": true,
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
      "description": "启动任务",
      "action": {
        "type": "KeyboardInput",
        "keys": ["win", "r"]
      },
      "next": {
        "success": "EndTask"
      },
      "delay": {
        "pre": 500,
        "cur": 1000,
        "post": 500
      },
      "limits": {
        "maxCount": 3
      }
    },
    "EndTask": {
      "type": "Input",
      "action": {
        "type": "KeyboardInput",
        "keys": ["esc"]
      },
      "description": "结束任务"
    }
  }
}
```
