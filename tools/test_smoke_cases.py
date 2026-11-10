import json
import unittest
from pathlib import Path

CASES = Path(__file__).resolve().parent / "smoke-cases.json"


class SmokeCaseTests(unittest.TestCase):
    def test_every_case_has_checkable_conditions(self):
        data = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertTrue(data["rubric"].strip())
        ids = [case["id"] for case in data["cases"]]
        self.assertEqual(len(ids), len(set(ids)), "Case ids must be unique")
        for case in data["cases"]:
            with self.subTest(case=case["id"]):
                for key in ("prompt", "observe", "pass", "fail"):
                    self.assertTrue(case.get(key), f"{case['id']} needs {key}")
                for key in ("pass", "fail"):
                    self.assertTrue(all(item.strip() for item in case[key]))


if __name__ == "__main__":
    unittest.main()
