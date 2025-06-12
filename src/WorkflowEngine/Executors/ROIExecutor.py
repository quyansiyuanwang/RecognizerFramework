from typing import Any

import cv2
import numpy as np
import pyautogui

from src.Structure import Action, Delay
from src.Typehints import GlobalsDict

from ..Controller import InputController, LogLevel, SystemController, global_log_manager
from ..exceptions import MatchingError, ROIError, TemplateError
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("ROI")
class ROIExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def main(self, delay: Delay, action: Action) -> str:
        # 0. 读取region
        region = self.job.get("region", {})
        x: int = int(region.get("x", 0))
        y: int = int(region.get("y", 0))
        w: int = int(region.get("width", 0))
        h: int = int(region.get("height", 0))

        # 1. 截屏
        roi = cv2.cvtColor(
            np.array(pyautogui.screenshot(region=(x, y, w, h) if region else None)),
            cv2.COLOR_RGB2BGR,
        )

        # 2. 读取模板图
        template_path: str = self.job["image"]["path"]
        confidence: float = self.job["image"].get("confidence", 1.0)
        template = cv2.imread(template_path)
        if template is None:  # type: ignore[union-attr]
            raise TemplateError(
                job=self.job,
                message=f"Template image not found at path: {template_path}",
            )
        if roi.shape[0] < template.shape[0] or roi.shape[1] < template.shape[1]:
            global_log_manager.log(
                "ROI区域小于模板, 自动使用全图进行匹配。",
                [LogLevel.WARNING],
                debug=self.globals.get("debug", False),
            )
            roi = cv2.cvtColor(
                np.array(pyautogui.screenshot()),
                cv2.COLOR_RGB2BGR,
            )
            if roi.shape[0] < template.shape[0] or roi.shape[1] < template.shape[1]:
                raise ROIError(
                    job=self.job,
                    message="ROI region is smaller than the template image, cannot match.",
                )

        # 3. 匹配
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(roi_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val < confidence:
            raise MatchingError(
                job=self.job,
                message=f"No match found in region with confidence >= {confidence}",
            )

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

        # 默认点击位置
        click_x = target_x
        click_y = target_y

        # 5. 执行动作, 如果有position, 做点击偏移
        if action:
            pos = action.get("position", {})
            if pos.get("type", "Relative") == "Relative":
                click_x = target_x + int(pos.get("x", 0))
                click_y = target_y + int(pos.get("y", 0))
            elif pos.get("type", "Relative") == "Absolute":
                click_x = int(pos.get("x", target_x))
                click_y = int(pos.get("y", target_y))

            InputController.click(
                x=click_x,
                y=click_y,
                delay_ms=delay.get("cur", 0),
                debug=self.globals.get("debug", False),
                ignore=self.globals.get("ignore", False),
            )

        return (
            f"Matched at ({target_x}, {target_y}), click at ({click_x}, {click_y})"
            f", confidence: {max_val}"
            if action
            else "No action specified"
        )

    def execute(self, *args: Any, **kwargs: Any) -> str:
        delay: Delay = self.job.get("delay", {})
        pre_delay: int = delay.get("pre", 0)
        post_delay: int = delay.get("post", 0)
        action = self.job.get("action", {})

        SystemController.sleep(pre_delay, debug=self.globals.get("debug", False))
        try:
            res: str = self.main(delay, action)
        except Exception as e:
            raise e
        finally:
            SystemController.sleep(post_delay, debug=self.globals.get("debug", False))
        return res
