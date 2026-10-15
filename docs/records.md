# 工作日志与卡片

## 记录位置

| 内容 | 位置与命名示例 |
| --- | --- |
| 每日工作日志 | `docs/logs/YYYY/MM/YYYY-MM-DD.jsonl`及同名Markdown摘要 |
| 2.6/2.7提纲或正文 | `docs/ch02/02-06-...`、`docs/ch02/02-07-...` |
| 来源索引与阅读笔记 | `docs/references/ch02/00-资料索引.md`、`notes/` |
| 实验计划与报告 | `reports/ch02/E02-07-YYYYMMDD-01/` |
| 模型版本记录 | `02-onnx-baseline/docs/model-version.md` |
| 本地大文件 | `02-onnx-baseline/data/`、`model/`、`outputs/` |

## 记录原则

日志记录目的、输入版本、实际完成、产出位置、实际检查和下一步；不复制资料卡或正文全文。JSONL事件遵循[日志格式](logging-schema.md)，Markdown只提供阅读摘要。

模型与实验记录至少包含Git提交、模型定义、权重来源、样例输入、前处理、导出参数、软件版本、运行命令、输出位置和检查结果。没有执行的步骤不写成已完成。

完整数据、权重、ONNX和大量输出不进入Git；报告用清单、大小、SHA256和本地相对位置关联它们。作者确认、AI检查与外部审核分别记录。
