# 项目结构说明

本项目的文件夹和文件构成如下：

## 根目录

- **`environment.yml`**: 项目环境配置文件，用于定义依赖包和环境(conda)。

- **`main.py`**: 项目的主入口文件。

- **`requirement.txt`**: Python 项目的依赖包列表。

- **`test.py`**: 测试脚本。

## `doc/`

- **`develop/structure.MD`**: 项目结构说明文档。

- **`manual/JsonField.MD`**: JSON 字段使用文档，详细描述了 JSON 配置的字段和用法。

## `script/`

- **`__main__.py`**: 脚本的主入口，可以使用`python -m script`执行主脚本。

- **`check_type.py`**: 类型检查相关脚本。

- **`format.py`**: 格式化工具。

- **`import_sort.py`**: 导入排序工具。

- **`schema.py`**: JSON Schema 相关脚本。

- **`workflows.json`**: 工作流配置文件。

- **`util/`**: 工具模块，包含通用工具函数。

- **`workflows.json`**: 脚本工作流文件。

## `src/`

- 项目核心代码。

  - **`Structure/`**: 定义了项目的核心结构体模块。

    - **`action.py`**: 动作结构体。

    - **`delay.py`**: 延时结构体。

    - **`image.py`**: 图片结构体。

    - **`job.py`**: 任务结构体。

    - **`limits.py`**: 限制结构体。

    - **`next.py`**: 任务流结构体。

    - **`position.py`**: 位置结构体。

    - **`region.py`**: 区域结构体。

  - **`Typehints/`**: 类型提示模块。

    - **`workflow.py`**: 工作流相关类型定义。

    - **`workflow_pydantic.py`**: 使用 Pydantic 定义的类型。

    - **`structure.py`**: 结构相关类型定义。

  - **`Util/`**: 通用工具模块。

    - **`util.py`**: 工具函数集合。

  - **`WorkflowEngine/`**: 工作流引擎模块。

    - **`Controller/`** : 子模块，包含控制器和执行器的实现。

      - **`InputController.py`**: 基础控制器类，定义了所有控制器的通用接口。

      - **`LogController.py`**: 日志管理模块，负责统一处理管理日志记录。

      - **`Runner.py`**: 工作流运行器，负责执行语句。

      - **`SystemController.py`**: 系统控制器，处理系统级或者 CPU 级任务（如启动程序）。

    - **`Executors/`**: 执行器模块，包含不同类型的执行器。

      - **`InputExecutor.py`**: 输入执行器，处理输入相关任务。

      - **`OCRExecutor.py`**: OCR 执行器，处理光学字符识别任务。

      - **`ROIExecutor.py`**: 区域操作执行器，处理图像区域相关任务。

      - **`SystemExecutor.py`**: 系统操作执行器，处理系统级相关任务。

    - **`executor.py`**: 执行器逻辑。

    - **`manager.py`**: 工作流管理器。

    - **`exceptions.py`**: 自定义异常。

## `workflow/`

- 包含工作流配置文件。

  - **`schema/`**: JSON Schema 文件夹。

    - **`generated.schema.json`**: 根据`Typehints/workflow_pydantic.py`自动生成的 Schema 文件。
