# 项目结构说明

本项目采用模块化设计，分为核心代码、脚本工具、文档、配置等部分，便于维护和扩展。以下为最新的详细目录和文件说明：

## 根目录

- **main.py**：项目主入口，启动整体流程。
- **environment.yml**：conda 环境依赖配置，便于一键创建开发环境。
- **requirement.txt**：pip 依赖包列表，适用于 pip 环境。
- **test.py**：测试脚本，快速验证主要功能。

## docs/ 文档目录

- **develop/Structure.MD**：项目结构说明（本文件）。
- **manual/JsonField.MD**：JSON 配置字段详细说明，包含所有可用字段、类型、示例。

## script/ 脚本与工具

- **\_\_main\_\_.py**：脚本主入口，支持 `python -m script` 执行批量工具（类型注解完善）。
- **check_type.py**：类型检查工具，辅助开发时类型安全。
- **format.py**：代码格式化工具，统一代码风格。
- **import_sort.py**：导入排序工具，自动整理 import 顺序。
- **schema.py**：JSON Schema 相关脚本，自动生成/校验 schema。
- **workflows.json**：脚本工作流配置示例。
- **util/**：通用工具函数模块。
  - **util.py**：常用工具函数集合。

## src/ 核心代码

- **Models/**：数据模型模块，基于 Pydantic 的类型定义和 JSON 解析。

  - **globals.py**：全局配置模型。
  - **input.py**：输入任务模型。
  - **main.py**：工作流模型，包括 `Workflow`、`Job` 等核心定义。
  - **roi.py**：区域识别任务模型。
  - **system.py**：系统任务模型。

- **Typehints/**：类型提示与 Pydantic 类型定义。

  - **basic.py**：基础类型定义。
  - **roi.py**：ROI 类型定义。
  - **structure.py**：结构相关类型定义。

- **Util/**：通用工具函数。

  - **util.py**：常用工具函数集合。

- **WorkflowEngine/**：工作流引擎。
  - **executor.py**：执行器基类与注册逻辑（含异常处理和缓存优化）。
  - **manager.py**：工作流管理器，负责任务调度与状态管理（含异常处理优化）。
  - **Controller/**：控制器子模块。
    - **InputController.py**：输入控制器，封装鼠标/键盘操作。
    - **LogController.py**：日志管理，统一日志输出。
    - **Runner.py**：工作流运行器，调度任务。
    - **SystemController.py**：系统控制器，处理系统级任务。
  - **Exceptions/**：自定义异常定义。
    - **base.py**：基础异常类型。
    - **crash.py**：通用崩溃异常。
    - **critical.py**：关键异常类型。
    - **ignorable.py**：可忽略异常类型。
    - **execs/**：细分的执行异常。
      - **input.py**：输入相关异常。
      - **roi.py**：ROI 相关异常。
      - **roi_crash.py**：ROI 崩溃异常。
      - **system.py**：系统相关异常。
      - **system_crash.py**：系统崩溃异常。
  - **Executors/**：执行器模块。
    - **InputExecutor.py**：输入任务执行器。
    - **OCRExecutor.py**：OCR 任务执行器。
    - **ROIExecutor.py**：区域识别任务执行器（支持窗口捕获与调试）。
    - **SystemExecutor.py**：系统任务执行器。
  - **Util/**：引擎相关工具。
    - **executor_works.py**：执行器工作流工具。
    - **style.py**：样式工具。
    - **util.py**：引擎通用工具。

## tests/ 测试目录

- **test_manager.py**：主测试脚本。
- **\_\_init\_\_.py**：包初始化。
- **executor/**：预留执行器相关测试（当前为空）。
- **workflow/**：工作流相关测试用例。
  - **`year`-`month`-`day`T`hour`.`minute`/**：按时间分组的测试集。
    - **\*.json**：测试输入。
    - **\*.answer**：期望输出。

## tools/ 工具目录

- **\_\_init\_\_.py**、**\_\_main\_\_.py**：包初始化与主入口。
- **GitCheckDiff/**
  - **diff_only_docs.py**：仅检测 .md 文件变更的工具脚本。
- **SingleScripts/**
  - **all_commit.py**：提交历史相关工具。
  - **check_type.py**：类型检查脚本。
  - **clean.py**：清理缓存、临时文件等。
  - **export_env.py**：导出环境依赖。
  - **format.py**：代码格式化脚本。
  - **import_sort.py**：导入排序脚本。
  - **workflows.json**：工具工作流配置。
- **util/**
  - **util.py**：工具函数实现。
  - **\_\_init\_\_.py**：util 包初始化。

> 存放各类开发辅助工具，如脚本、插件等。

## workflow/ 工作流配置

- 各类工作流配置文件（\*.json），定义自动化流程。
- **schema/**：JSON Schema 文件夹。
  - **generated.schema.json**：根据 Pydantic 类型自动生成的 schema 文件。
- **tests/**：工作流相关测试用例。

---

> 各模块职责清晰，便于扩展和维护。建议开发者优先查阅 `src/` 及 `doc/manual/JsonField.MD` 以了解核心逻辑和配置方法。
