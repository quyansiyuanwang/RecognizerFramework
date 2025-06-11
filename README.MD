# RecogniorFramework

RecogniorFramework 是一个模块化的工作流引擎框架，旨在通过 JSON 配置文件定义任务流，支持多种任务类型（如区域识别、文字识别、输入操作、系统操作等），并提供灵活的扩展能力。

## 功能特性

- **模块化设计**：通过结构化的模块（如任务、动作、延时等）实现高内聚、低耦合。
- **多任务类型支持**：
  - 区域识别（ROI）
  - 光学字符识别（OCR）
  - 输入操作（键盘、鼠标）
  - 系统操作（延时、日志记录等）
- **JSON 配置驱动**：通过简单的 JSON 文件定义任务流，支持继承、分支、依赖等高级特性。
- **日志管理**：支持多级别日志输出（DEBUG、INFO、WARNING、ERROR 等），并支持彩色日志和文件记录。
- **可扩展性**：通过自定义执行器和控制器，轻松扩展框架功能。

---

## 快速开始

### 环境配置

1. 安装依赖：

   ```bash
   conda env create -f environment.yml
   conda activate RecogniorFramework
   ```

2. 或使用 `pip` 安装：

   ```bash
   pip install -r requirement.txt
   ```

### 运行示例工作流

1. 编辑 `workflow/example.json` 文件，定义任务流。
2. 执行以下命令运行工作流：

   ```bash
   python main.py workflow/example.json
   ```

---

## JSON 配置说明

工作流通过 JSON 文件定义，以下是主要字段的说明：

### 顶层字段

- **`begin`**：起始任务名，必须是 `jobs` 中的一个 key。
- **`globals`**：全局配置，影响所有任务。
  - `debug`：是否开启调试模式。
  - `logConfig`：日志配置（如日志级别、文件路径等）。

### `Job` 字段

- **`type`**：任务类型（如 `ROI`、`OCR`、`Input`、`System` 等）。
- **`action`**：任务的具体动作（如键盘输入、鼠标点击等）。
- **`next`**：下一个任务名或分支（支持 `success`/`failure` 分支）。
- **`delay`**：延时设置（任务前中后的等待时间）。
- **`limits`**：任务执行限制（如最大执行次数、失败次数等）。

更多详细说明请参考 [JSON 字段使用文档](doc/manual/JsonField.MD)。

---

## 示例 JSON

以下是一个简单的工作流示例：

```json
{
  "$schema": "./schema/generated.schema.json",
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

---

## 项目结构

以下是项目的主要目录和文件说明：

### 根目录

- **`main.py`**：项目的主入口文件，用于执行工作流。
- **`environment.yml`**：项目环境配置文件，用于定义依赖包和环境（适用于 Conda）。
- **`requirement.txt`**：Python 项目的依赖包列表。
- **`README.MD`**：项目的主文档（即本文件）。
- **`test.py`**：测试脚本。

### `doc/`

- **`manual/JsonField.MD`**：JSON 字段使用文档，详细描述了 JSON 配置的字段和用法。
- **`develop/Structure.MD`**：项目结构说明文档，介绍了项目的文件夹和模块构成。

### `script/`

- **`__main__.py`**：脚本的主入口，可以使用 `python -m script` 执行主脚本。
- **`check_type.py`**：类型检查脚本。
- **`format.py`**：代码格式化脚本。
- **`import_sort.py`**：导入排序脚本。
- **`schema.py`**：JSON Schema 生成脚本。
- **`workflows.json`**：脚本工作流配置文件。

### `src/`

- **`Structure/`**：定义了项目的核心结构体模块（如任务、动作、延时等）。
- **`Typehints/`**：类型提示模块，包含工作流和结构体的类型定义。
- **`Util/`**：通用工具模块，提供字典过滤等工具函数。
- **`WorkflowEngine/`**：工作流引擎模块，包含控制器、执行器、管理器和异常处理等核心逻辑。

### `workflow/`

- **`example.json`**：示例工作流配置文件。
- **`schema/`**：JSON Schema 文件夹，用于验证工作流配置文件的合法性。

更多详细说明请参考 [项目结构文档](doc/develop/Structure.MD)。

---

## 贡献指南

欢迎对本项目提出改进建议或提交代码贡献！请确保遵循以下步骤：

1. Fork 本仓库并创建分支。
2. 提交代码前运行以下命令进行代码检查和格式化：

   ```bash
   python -m script pre-commit
   ```

3. 提交 Pull Request 并描述您的更改。

---

## 联系方式

如有任何问题或建议，请通过 Issue 提交反馈。
