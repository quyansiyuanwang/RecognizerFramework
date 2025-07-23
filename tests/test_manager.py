"""
This file is mainly tests for the file `src/WorkflowEngine/manager.py`.
"""

import unittest

from src.WorkflowEngine import WorkflowManager


class TestWorkflowManager(unittest.TestCase):
    def setUp(self):
        self.target_file = "tests/workflow/2025-07-23T06.47/test_read.json"
        self.answer_file = "tests/workflow/2025-07-23T06.47/test_read.json.answer"

        self.manager = WorkflowManager(self.target_file)

        self.__write_mode = False
        if self.__write_mode:
            self.write_answer()
            assert True, "Write mode is enabled"

    def write_answer(self):
        if not self.__write_mode:
            return

        repred = repr(self.manager)
        with open(self.answer_file, "w", encoding="utf-8") as f:
            f.write(repred)

    def test_load_workflow(self):
        repred = repr(self.manager)
        with open(self.answer_file, "r", encoding="utf-8") as f:
            ans = f.read()

        self.assertEqual(repred, ans)
