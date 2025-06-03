from typing import Any

import cv2

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("Image")
class ImageExecutor(Executor):
    def execute(self, job: Job) -> Any:
        image_path: str = job["image"]["path"]
        if not image_path:
            raise ValueError("Image path is required for ImageExecutor.")

        # Load the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:  # type: ignore[comparison-overlap]
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        # Here you can add any image processing logic you need
        # For demonstration, we will just return the shape of the image
        return f"Processed Image: {job['description']}, Shape: {image.shape}"
