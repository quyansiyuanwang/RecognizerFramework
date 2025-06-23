# 项目结构说明

本项目采用模块化设计，分为核心代码, 脚本工具, 文档, 配置等部分，便于维护和扩展. 以下为最新的详细目录和文件说明：

## 根目录

- **main.py**：项目主入口，启动整体流程.
- **environment.yml**：conda 环境依赖配置，便于一键创建开发环境.
- **requirement.txt**：pip 依赖包列表，适用于 pip 环境.
- **test.py**：测试脚本，快速验证主要功能.

## doc/ 文档目录

- **develop/Structure.MD**：项目结构说明(本文件).
- **manual/JsonField.MD**：JSON 配置字段详细说明，包含所有可用字段, 类型, 示例.

## script/ 脚本与工具

- \***\*main**.py\*\*：脚本主入口，支持 `python -m script` 执行批量工具.
- **check_type.py**：类型检查工具，辅助开发时类型安全.
- **format.py**：代码格式化工具，统一代码风格.
- **import_sort.py**：导入排序工具，自动整理 import 顺序.
- **schema.py**：JSON Schema 相关脚本，自动生成/校验 schema.
- **workflows.json**：脚本工作流配置示例.
- **util/**：通用工具函数模块.
  - **util.py**：常用工具函数集合.

## src/ 核心代码

- **Structure/**：核心结构体定义.

  - **action.py**：动作结构体，描述单步操作.
  - **after.py**：后置任务结构体.
  - **Base.py**：结构体基类.
  - **delay.py**：延时结构体，定义任务前后延时.
  - **input.py**：输入结构体.
  - **job.py**：任务结构体，描述单个任务的所有属性.
  - **keyboard.py**：键盘输入结构体.
  - **limits.py**：限制结构体，控制任务执行次数等.
  - **mouse.py**：鼠标输入结构体.
  - **next.py**：任务流结构体，描述任务流转逻辑.
  - **region.py**：区域结构体，描述屏幕区域.
  - **roi.py/roi_image.py**：区域识别相关结构体.
  - **system.py**：系统操作结构体.
  - **text.py**：文本输入结构体.
  - **TypeMap.py/Util.py**：类型映射与结构体工具.

- **Typehints/**：类型提示与 Pydantic 类型定义.

  - **structure.py**：结构相关类型定义.
  - **pydantic_pkg/**：各功能领域的 Pydantic 类型包(如 input, roi, system 等).
  - **framework/**：框架相关类型定义.

- **Util/**：通用工具函数.

  - **util.py**：常用工具函数集合.

- **WorkflowEngine/**：工作流引擎.
  - **executor.py**：执行器基类与注册逻辑.
  - **manager.py**：工作流管理器，负责任务调度与状态管理.
  - **Controller/**：控制器子模块.
    - **InputController.py**：输入控制器，封装鼠标/键盘操作.
    - **LogController.py**：日志管理，统一日志输出.
    - **Runner.py**：工作流运行器，调度任务.
    - **SystemController.py**：系统控制器，处理系统级任务.
  - **Executors/**：执行器模块.
    - **InputExecutor.py**：输入任务执行器.
    - **OCRExecutor.py**：OCR 任务执行器.
    - **ROIExecutor.py**：区域识别任务执行器.
    - **SystemExecutor.py**：系统任务执行器.
  - **Exceptions/**：自定义异常定义.
    - **base/**：基础异常类型，所有自定义异常的父类，便于统一捕获和扩展.
    - **crash/**：通用异常类型(如 ActionTypeError 等)，用于处理执行时的类型错误、参数错误等.
    - **critical/**：关键异常类型，表示必须中断流程的严重错误.
    - **execs/**：细分的执行异常(如 roi.py、input.py、system.py)，分别对应 ROI、输入、系统等模块的专属异常类型.
    - **ignorable/**：可忽略异常类型，遇到时可选择跳过而不中断主流程.
  - **Util/**：引擎相关工具.

## workflow/ 工作流配置

- 各类工作流配置文件(\*.json)，定义自动化流程.
- **schema/**：JSON Schema 文件夹.
  - **generated.schema.json**：根据 Pydantic 类型自动生成的 schema 文件.
- **tests/**：工作流相关测试用例.

## images/ 资源目录

- 项目用到的图片资源，按业务/模块分类存放.
- 如 `wechat.png`, `win.png` 等.

## log/ 日志目录

- 运行日志文件输出目录，如 `example.log`, `test.log`.

---

> 各模块职责清晰，便于扩展和维护. 建议开发者优先查阅 `src/` 及 `doc/manual/JsonField.MD` 以了解核心逻辑和配置方法.
