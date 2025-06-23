import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json

from src.Typehints import Workflow

with open("workflow/schema/generated.schema.json", "w", encoding="utf-8") as f:
    json.dump(Workflow.model_json_schema(), f, indent=2, ensure_ascii=False)
