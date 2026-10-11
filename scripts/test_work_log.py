"""工作日志契约测试：缺字段、时间、来源篡改、文段和路径边界。"""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from validate_work_log import Draft202012Validator, FormatChecker, ROOT, validate_event


class WorkLogContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = json.loads((ROOT / "docs/schemas/work-event.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema, format_checker=FormatChecker())
        cls.example = json.loads((ROOT / "docs/templates/examples/passage-generated.example.json").read_text(encoding="utf-8"))

    def test_valid_example_and_snapshots(self):
        validate_event(self.example, self.validator)

    def test_reject_invalid_or_tampered_records(self):
        changes = {
            "missing-agent": lambda x: x["actor"].update(agent_id=None),
            "missing-prompt": lambda x: x.update(prompt=None),
            "missing-timezone": lambda x: x.update(recorded_at="2026-10-11T00:00:00"),
            "reversed-time": lambda x: x.update(completed_at="2026-10-10T23:59:59+08:00"),
            "requested-fast": lambda x: x["actor"]["model"]["requested"].update(fast_mode=True),
            "tampered-prompt": lambda x: x["prompt"]["full_prompt"].update(sha256="0" * 64),
            "tampered-passage": lambda x: x["outputs"][0]["target"].update(text_sha256="0" * 64),
            "missing-block": lambda x: x["outputs"][0]["target"].update(block_id="missing-block"),
            "path-escape": lambda x: x["outputs"][0]["snapshot"].update(path="../outside.md"),
            "confirmation-without-record": lambda x: x["review"].update(status="author_confirmed"),
            "revision-without-parent": lambda x: x.update(event_type="passage_revised"),
            "unknown-field": lambda x: x.update(agentid="bad"),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                event = deepcopy(self.example)
                change(event)
                with self.assertRaises((ValueError, OSError)):
                    validate_event(event, self.validator)

    def test_configuration_examples(self):
        profiles = {
            "03-transfer-learning/configs/linux-autodl-train.example.json": "cuda:0",
            "03-transfer-learning/configs/windows-cpu-test.example.json": "cpu",
            "04-lightweight/configs/windows-cpu-baseline.example.json": "cpu",
        }
        for path, device in profiles.items():
            with self.subTest(path=path):
                profile = json.loads((ROOT / path).read_text(encoding="utf-8"))
                self.assertTrue(profile["strict_device"])
                self.assertEqual(profile["device"], device)
                self.assertEqual(profile["status"], "configuration_example_only")


if __name__ == "__main__":
    unittest.main()
