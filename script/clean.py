import os
import re
import shutil
from typing import List


def clean_pycache(root_dir: str, patterns: List[str]):
    for dirpath, dirnames, _ in os.walk(root_dir):
        # 正则匹配并删除目录
        to_remove: List[str] = []
        for dirname in dirnames:
            for pattern in patterns:
                if re.fullmatch(pattern, dirname):
                    to_remove.append(dirname)
                    break
        for dirname in to_remove:
            target_path = os.path.join(dirpath, dirname)
            shutil.rmtree(target_path, ignore_errors=True)
            print(f"Removed: {target_path}")
        # 从dirnames中移除已删除的目录, 防止os.walk递归进入
        dirnames[:] = [d for d in dirnames if d not in to_remove]


if __name__ == "__main__":
    clean_pycache(
        os.getcwd(),
        patterns=[
            "__pycache__",
            "build",
            ".pytest_cache",
        ],
    )
