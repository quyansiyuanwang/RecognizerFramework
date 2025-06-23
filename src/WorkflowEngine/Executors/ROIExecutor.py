from typing import Any

import cv2
import numpy as np
import pyautogui

from src.Structure import ROI, Delay
from src.Typehints import GlobalsDict
from src.WorkflowEngine.Exceptions.crash import ActionTypeError, TemplateError
from src.WorkflowEngine.Exceptions.execs.roi import MatchingError, ROIError

from ..Controller import InputController, LogLevel, SystemController, global_log_manager
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("ROI")
class ROIExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def main(self, roi: ROI) -> str:
        # 0. 读取region
        region = roi.get("region", {})
        x: int = int(region.get("x", 0))
        y: int = int(region.get("y", 0))
        w: int = int(region.get("width", 0))
        h: int = int(region.get("height", 0))

        # 1. 截屏
        mat = cv2.cvtColor(
            np.array(pyautogui.screenshot(region=(x, y, w, h) if region else None)),
            cv2.COLOR_RGB2BGR,
        )

        # 2. 读取模板图
        template_path: str = roi["image"]["path"]
        confidence: float = roi["image"].get("confidence", 1.0)
        template = cv2.imread(template_path)
        if template is None:  # type: ignore[union-attr]
            raise TemplateError(
                job=self.job,
                message=f"Template image not found at path: {template_path}",
            )
        if mat.shape[0] < template.shape[0] or mat.shape[1] < template.shape[1]:
            global_log_manager.log(
                "ROI区域小于模板, 自动使用全图进行匹配。",
                [LogLevel.WARNING],
                debug=self.globals.get("debug", False),
            )
            mat = cv2.cvtColor(
                np.array(pyautogui.screenshot()),
                cv2.COLOR_RGB2BGR,
            )
            if mat.shape[0] < template.shape[0] or mat.shape[1] < template.shape[1]:
                raise ROIError(
                    job=self.job,
                    message="ROI region is smaller than the template image, cannot match.",
                )

        # 3. 匹配
        mat_gray = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(mat_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val < confidence:
            raise MatchingError(
                job=self.job,
                message=f"No match found in region with confidence >= {confidence}",
            )

        # action Factory
        if roi.get("type") == "DetectOnly":
            global_log_manager.log(
                f"ROI detected at {max_loc} with confidence {max_val}",
                [LogLevel.DEBUG],
                debug=self.globals.get("debug", False),
            )
            return f"Detected at {max_loc} with confidence {max_val}"

        elif roi.get("type") == "MoveMouse":
            # 4. 计算点击点
            top_left = max_loc
            h_temp, w_temp = template_gray.shape

            # 默认点击模板中心
            target_x = top_left[0] + w_temp // 2
            target_y = top_left[1] + h_temp // 2

            # 加上region偏移
            target_x += int(region.get("x", 0))
            target_y += int(region.get("y", 0))

            global_log_manager.log(
                f"ROI match: location={(target_x, target_y)}, confidence={max_val}, template={template_path}",
                [LogLevel.DEBUG],
                debug=self.globals.get("debug", False),
            )

            # 移动鼠标
            duration: int = roi.get("duration", 0)
            InputController.move_to(
                x=target_x,
                y=target_y,
                duration=duration,
                debug=self.globals.get("debug", False),
                ignore=self.globals.get("ignore", False),
            )

            return f"Matched at ({target_x}, {target_y})" f", confidence: {max_val}"
        else:
            raise ActionTypeError(
                job=self.job,
                message=f"Unsupported ROI type: {roi.get('type')}",
            )

    def execute(self, *args: Any, **kwargs: Any) -> str:
        delay: Delay = self.job.get("delay", {})
        pre_delay: int = delay.get("pre", 0)
        post_delay: int = delay.get("post", 0)
        roi: ROI = self.job.get("roi", {})

        SystemController.sleep(
            pre_delay,
            debug=self.globals.get("debug", False),
            prefix="ROIExecutorPreDelay",
        )
        try:
            res: str = self.main(roi)
        except Exception as e:
            raise e
        finally:
            SystemController.sleep(
                post_delay,
                debug=self.globals.get("debug", False),
                prefix="ROIExecutorPostDelay",
            )
        return res
