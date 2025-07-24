# RecognizerFramework

![main language](https://img.shields.io/badge/python-3.13-blue?logo=python)
![platform](https://img.shields.io/badge/platform-windows-blueviolet.svg)
![license](https://img.shields.io/github/license/quyansiyuanwang/RecognizerFramework.svg)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/quyansiyuanwang/RecognizerFramework/checks.yml)
![main drive](https://img.shields.io/badge/drive-json-brightgreen.svg)
![repo size](https://img.shields.io/github/repo-size/quyansiyuanwang/RecognizerFramework)
![last commit](https://img.shields.io/github/last-commit/quyansiyuanwang/RecognizerFramework)
![doc last](https://img.shields.io/badge/docs%20last-2025--07--25-blue.svg)

RecognizerFramework 是一个模块化的工作流引擎框架，支持通过 JSON 配置文件定义自动化任务流，涵盖区域识别、输入操作、系统操作等多种任务类型，并具备良好的扩展性和可维护性。

---

## 功能特性

- **模块化设计**：核心结构体、控制器、执行器分层，便于扩展和维护。
- **多任务类型支持**：支持区域识别（ROI）、OCR、输入（键盘/鼠标）、系统操作等。
- **JSON 配置驱动**：通过 JSON 文件灵活定义任务流，支持分支、依赖、延时、限制等高级特性。
- **日志管理**：多级别日志输出（DEBUG/INFO/WARNING/ERROR/CRITICAL），支持彩色和文件日志。
- **类型安全**：基于 Pydantic 类型校验，保障配置和运行安全。
- **可扩展性**：支持自定义执行器、控制器和异常类型。

---

## 快速开始

### 环境配置

1. 安装依赖：

   ```bash
   conda env create -f environment.yml
   conda activate RecognizerFramework
   ```

2. 或使用 pip 安装：

   ```bash
   pip install -r requirements.txt
   ```

### 运行示例工作流

1. 编辑 `workflow/example.json` 文件，定义任务流。
2. 执行以下命令运行工作流：

   ```bash
   python main.py workflow/example.json
   ```

---

## JSON 配置说明

工作流通过 JSON 文件定义，主要字段如下：

### 顶层字段

- **begin**：起始任务名，必须是 jobs 中的一个 key。
- **globals**：全局配置，影响所有任务。
  - debug：是否开启调试模式。
  - colorful：是否彩色日志输出。
  - ignore：是否忽略错误。
  - logConfig：日志配置（如日志级别、文件路径、格式等）。
- **jobs**：所有任务节点，key 为任务名，value 为 Job 定义。

### Job 字段

- **type**：任务类型（如 ROI、OCR、Input、System、Overload 等）。
- **description**：任务描述。
- **before**：前置任务配置，支持 tasks、ignore_errors。
- **after**：后置任务配置，支持 success、failure、always、ignore_errors。
- **next**：下一个任务名或分支（支持 success/failure 分支）。
- **delay**：延时设置（pre、post）。
- **limits**：执行限制（maxCount、maxFailure、maxSuccess、exit）。
- **needs**：依赖的前置任务名。
- 任务类型相关字段（如 roi、input、system 等）详见 [JSON 字段使用文档](doc/manual/JsonField.MD)。

---

## 示例 JSON

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
      "description": "启动任务",
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

## 项目结构

详细结构请见 [项目结构文档](doc/develop/Structure.MD)。主要目录如下：

### 根目录

- main.py：项目主入口。
- environment.yml：conda 环境依赖配置。
- requirement.txt：pip 依赖包列表。

### doc/

- develop/Structure.MD：项目结构说明。
- manual/JsonField.MD：JSON 字段详细说明。

### script/

- **main.py**：脚本主入口。
- check_type.py、format.py、import_sort.py、schema.py：开发辅助工具。
- workflows.json：脚本工作流配置。
- util/：通用工具函数。

### src/

- Models/：数据模型模块。
- Structure/：核心结构体定义。
- Typehints/：类型提示与 Pydantic 类型定义。
- Util/：通用工具函数。
- WorkflowEngine/：工作流引擎（控制器、执行器、异常等）。

### workflow/

- 各类工作流配置文件（\*.json）。
- schema/：JSON Schema 文件夹。

### images/

- 项目用到的图片资源。

### log/

- 日志输出目录。

---

## 贡献指南

欢迎对本项目提出改进建议或提交代码贡献！请遵循以下流程：

1. Fork 本仓库并创建分支。
2. 提交代码前运行：

   ```bash
   python -m script pre-commit
   ```

3. 提交 Pull Request 并描述您的更改。

---

[![Contributors](https://contrib.rocks/image?repo=quyansiyuanwang/RecognizerFramework)](https://github.com/quyansiyuanwang/RecognizerFramework/graphs/contributors)

---

## 联系方式

如有任何问题或建议，请通过 Issue 提交反馈。
