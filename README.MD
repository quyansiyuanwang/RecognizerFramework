# RecognizerFramework

![main language](https://img.shields.io/badge/python-3.13-blue?logo=python)
![platform](https://img.shields.io/badge/platform-windows-blueviolet.svg)
![license](https://img.shields.io/github/license/quyansiyuanwang/RecognizerFramework.svg)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/quyansiyuanwang/RecognizerFramework/checks.yml)
![main drive](https://img.shields.io/badge/drive-json-brightgreen.svg)
![repo size](https://img.shields.io/github/repo-size/quyansiyuanwang/RecognizerFramework)
![last commit](https://img.shields.io/github/last-commit/quyansiyuanwang/RecognizerFramework)
![doc last](https://img.shields.io/badge/docs%20last-2025--09--26-blue.svg)

RecognizerFramework 是一个模块化的工作流引擎框架，支持通过 JSON 配置文件定义自动化任务流，涵盖区域识别、输入操作、系统操作等多种任务类型，并具备良好的扩展性和可维护性。

---

## 文档语言

[中文](./README.MD) | [English](./README.EN.MD)

---

## 功能特性

- **模块化设计**：核心结构体、控制器、执行器分层，便于扩展和维护。
- **多任务类型支持**：支持区域识别（ROI）、OCR、输入（键盘/鼠标）、系统操作、表达式计算（Calculate）等。
- **JSON 配置驱动**：通过 JSON 文件灵活定义任务流，支持分支、依赖、延时、限制等高级特性。
- **后台输入支持**：支持在不改变当前焦点的情况下向指定窗口发送输入（文本、键盘、鼠标）。
- **智能窗口查找**：支持按标题、类名、进程名查找窗口，支持精确匹配和模糊匹配。
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

- **type**：任务类型（如 ROI、OCR、Input、System、Overload、Calculate 等）。
- **description**：任务描述。
- **before**：前置任务配置，支持 tasks、ignore_errors。
- **after**：后置任务配置，支持 success、failure、always、ignore_errors。
- **next**：下一个任务名或分支（支持 success/failure 分支）。
- **delay**：延时设置（pre、post）。
- **limits**：执行限制（maxCount、maxFailure、maxSuccess、exit）。
- **needs**：依赖的前置任务名。
- 任务类型相关字段（如 roi、input、system、calculate 等）详见 [JSON 字段使用文档](/docs/zh-cn/manual/JsonField.MD)。

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
        "success": "BackgroundInputTask"
      },
      "delay": {
        "pre": 500,
        "post": 500
      }
    },
    "BackgroundInputTask": {
      "type": "Input",
      "description": "后台输入示例",
      "input": {
        "type": "Text",
        "background": true,
        "title": "记事本",
        "text": {
          "message": "这是后台输入的文本，不会改变当前焦点",
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

本项目采用模块化设计，分为核心代码、脚本工具、文档、配置等部分，便于维护和扩展。以下为主要目录和文件说明：

### 根目录

- **main.py**：项目主入口，启动整体流程。
- **environment.yml**：conda 环境依赖配置，便于一键创建开发环境。
- **requirement.txt**：pip 依赖包列表，适用于 pip 环境。
- **test.py**：测试脚本，快速验证主要功能。

### docs/ 文档目录

- **develop/Structure.MD**：项目结构说明。
- **manual/JsonField.MD**：JSON 配置字段详细说明。

### script/ 脚本与工具

- **\_\_main\_\_.py**：脚本主入口，支持 `python -m script` 执行批量工具。
- **check_type.py**、**format.py**、**import_sort.py**、**schema.py**：开发辅助工具。
- **workflows.json**：脚本工作流配置示例。
- **util/**：通用工具函数模块（含 util.py）。

### src/ 核心代码

- **Models/**：数据模型模块，基于 Pydantic 的类型定义和 JSON 解析。
- **Typehints/**：类型提示与 Pydantic 类型定义。
- **Util/**：通用工具函数。
- **WorkflowEngine/**：工作流引擎（含控制器、执行器、异常等子模块）。

### tests/ 测试目录

- **test_manager.py**、**\_\_init\_\_.py**、**executor/**、**workflow/**：主测试脚本及用例。

### tools/ 工具目录

- **\_\_init\_\_.py**、**\_\_main\_\_.py**：包初始化与主入口。
- **GitCheckDiff/**：diff_only_docs.py 等工具脚本。
- **SingleScripts/**：all_commit.py、check_type.py、clean.py、export_env.py、format.py、import_sort.py、workflows.json。
- **util/**：util.py、\_\_init\_\_.py。

> 存放各类开发辅助工具，如脚本、插件等。

### workflow/ 工作流配置

- 各类工作流配置文件（\*.json），定义自动化流程。
- **schema/**：JSON Schema 文件夹。

---

## 贡献指南

欢迎对本项目提出改进建议或提交代码贡献！请遵循以下流程：

1. Fork 本仓库并创建分支。
2. 提交代码前运行：

   ```bash
   python -m script commit
   ```

   ```bash
   python -m tools all
   ```

3. 提交 Pull Request 并描述您的更改。

---

## 文档

- **[JSON 字段说明文档](/docs/zh-cn/manual/JsonField.MD)** - 详细的配置字段说明
- **[项目结构文档](/docs/zh-cn/develop/Structure.MD)** - 项目代码结构说明

---

[![Contributors](https://contrib.rocks/image?repo=quyansiyuanwang/RecognizerFramework)](https://github.com/quyansiyuanwang/RecognizerFramework/graphs/contributors)

---

## 联系方式

如有任何问题或建议，请通过 Issue 提交反馈。
