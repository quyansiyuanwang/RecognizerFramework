"""
This file is mainly tests for the file `src/WorkflowEngine/manager.py`.
"""

import os
import sys
import unittest

from src.main import run


class TestWorkflowManager(unittest.TestCase):
    def setUp(self):
        self.target_file = "tests/workflow/2025-07-25T11.06/calculate.json"
        self.answer_file = "tests/workflow/2025-07-25T11.06/calculate.json.answer"

        self.__write_mode = False
        if self.__write_mode:
            self.write_answer()
            assert True, "Write mode is enabled"

    def write_answer(self):
        if not self.__write_mode:
            return

        with open(self.answer_file, "w", encoding="utf-8") as f:
            sys.stdout = f
            run(self.target_file)
            sys.stdout = sys.__stdout__  # 恢复标准输出

    def test_load_workflow(self):
        with open("./TEST-CALCULATE.tmp", "w+", encoding="utf-8") as f:
            sys.stdout = f
            run(self.target_file)
            sys.stdout = sys.__stdout__

            f.seek(0)  # Move the cursor to the beginning of the file
            reply = f.read()

        with open(self.answer_file, "r", encoding="utf-8") as f:
            ans = f.read()

        self.assertEqual(reply, ans)

    def tearDown(self) -> None:
        if os.path.exists("./TEST-CALCULATE.tmp"):
            os.remove("./TEST-CALCULATE.tmp")
