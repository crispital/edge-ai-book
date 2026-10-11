"""校验 JSON/JSONL 工作事件、提示词快照和文段来源；不执行写作或模型代码。"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    raise SystemExit("缺少 jsonschema，请先安装 requirements-dev.txt。")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/schemas/work-event.schema.json"


def resolve_path(path):
    candidate = (ROOT / path).resolve()
    if not candidate.is_relative_to(ROOT):
        raise ValueError(f"路径超出仓库: {path}")
    return candidate


def read_artifact(artifact):
    if artifact["git_commit"]:
        data = subprocess.run(
            ["git", "show", artifact["git_commit"] + ":" + artifact["path"]],
            cwd=ROOT, check=True, capture_output=True
        ).stdout
    else:
        data = resolve_path(artifact["path"]).read_bytes()
    if artifact["hash_mode"] == "sha256_utf8_lf":
        data = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    if hashlib.sha256(data).hexdigest() != artifact["sha256"]:
        raise ValueError(f"快照校验值不一致: {artifact['path']}")
    return data


def check_passage(data, target):
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    begin = f"<!-- d2el:block {target['block_id']} -->"
    end = "<!-- /d2el:block -->"
    matches = re.findall(re.escape(begin) + r"\n(.*?)\n" + re.escape(end), text, re.S)
    if len(matches) != 1:
        raise ValueError(f"文段标记必须唯一且成对: {target['block_id']}")
    if hashlib.sha256(matches[0].encode("utf-8")).hexdigest() != target["text_sha256"]:
        raise ValueError(f"文段内容校验值不一致: {target['block_id']}")


def validate_event(event, validator, metadata_only=False):
    errors = sorted(validator.iter_errors(event), key=lambda e: str(list(e.path)))
    if errors:
        raise ValueError("; ".join(f"{list(e.path)}: {e.message}" for e in errors))
    if event["started_at"] and event["completed_at"]:
        start = datetime.fromisoformat(event["started_at"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(event["completed_at"].replace("Z", "+00:00"))
        if end < start:
            raise ValueError("completed_at 早于 started_at")
    if metadata_only:
        return
    artifacts = list(event["inputs"])
    if event["prompt"]:
        artifacts.append(event["prompt"]["full_prompt"])
    for artifact in artifacts:
        read_artifact(artifact)
    for output in event["outputs"]:
        data = read_artifact(output["snapshot"])
        target = output["target"]
        if target:
            check_passage(data, target)
            if target["git_commit"]:
                target_data = subprocess.run(
                    ["git", "show", target["git_commit"] + ":" + target["path"]],
                    cwd=ROOT, check=True, capture_output=True
                ).stdout
                check_passage(target_data, target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="仓库相对路径，JSON对象或逐行JSONL")
    parser.add_argument("--metadata-only", action="store_true", help="只查schema，不核对证据文件")
    args = parser.parse_args()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    seen = set()
    count = 0
    for name in args.files:
        path = resolve_path(name)
        text = path.read_text(encoding="utf-8")
        events = [json.loads(line) for line in text.splitlines() if line.strip()] if path.suffix == ".jsonl" else [json.loads(text)]
        if not events:
            raise ValueError(f"日志没有事件: {name}")
        for event in events:
            validate_event(event, validator, args.metadata_only)
            if path.is_relative_to(ROOT / "docs/logs") and event["record_kind"] != "actual":
                raise ValueError("正式日志禁止写入 example 事件")
            if event["event_id"] in seen:
                raise ValueError(f"重复事件ID: {event['event_id']}")
            seen.add(event["event_id"])
            count += 1
    mode = "仅元信息" if args.metadata_only else "含证据文件与文段"
    print(f"验证通过: {count} 个事件（{mode}）。不代表人工确认或事实验收。")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"验证失败: {exc}", file=sys.stderr)
        raise SystemExit(1)
