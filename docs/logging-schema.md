# JSON 工作日志与文段溯源

## 格式与文件

JSON Schema是使用的标准；事件字段、JSONL归档、ID和文段标记是按作者溯源要求设计的项目约定，不是指南提供的日志标准。

采用 [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)，项目 schema 为 [work-event.schema.json](schemas/work-event.schema.json)，版本 1.0.0。

正式结构化日志保存为 docs/logs/YYYY/MM/YYYY-MM-DD.jsonl，每行一个 JSON 对象。Markdown 日志保留阅读摘要，不代替 JSONL 事件；新记录以 JSONL 为依据。原有初始化 Markdown 记录保留，不猜测缺失时间补造历史事件。

事件 ID 沿用 LYYYYMMDD-序号，跨 Markdown 与 JSONL 使用同一个事件 ID。示例只能放 templates，不可加入正式日志。

## 必须能够回答什么

| 问题 | 字段 |
| --- | --- |
| 何时记录，任务何时开始和结束 | recorded_at、started_at、completed_at，带时区的 ISO 8601 |
| 谁执行，真实 subagent 身份是什么 | actor.kind、name、agent_id |
| 请求什么模型，实际设置是否已知 | actor.model.requested、actual；未知实际字段为 null |
| 对应哪个小节和什么任务 | task.section、summary |
| 工作基于哪份稿件或代码 | git.branch、base_commit；inputs 的版本与校验值 |
| 用了哪套提示词及具体填充内容 | prompt 的 run_id、template_id、template_version、full_prompt |
| 哪个文段由它生成，生成了什么 | outputs 的不可覆盖 snapshot、target.block_id、text_sha256 |
| 放到了哪份稿件中 | target.path、git_commit |
| 谁核对，是否已经确认 | review；未经确认保持 unreviewed |
| 后续改写从哪里来 | related_event_ids，与原始生成事件关联 |
| 做了哪些检查、哪些没做 | checks，分别标 passed/failed/not_run |

schema 规定字段、类型和必填条件；快照校验值用于后续核对内容，不能单凭填了字段就证明调用真实发生，也不代替作者核验。

## 文段生成记录

每次实际 subagent 生成文本，追加 event_type=passage_generated 的事件。该类型强制：
- actor.kind=subagent，真实 agent ID 与请求模型配置齐全。
- 记录真实起止时间、完整填充提示词文件及 SHA256。
- 至少一个输出文段，指定稳定 block ID 和文段文本 SHA256。
- 输出快照保留；作者确认状态与生成状态分开。

每个文段在输出快照中使用标记：
```markdown
<!-- d2el:block p02-07-001 -->
[这段的实际内容]
<!-- /d2el:block -->
```

多个文段同次生成时，在同一事件 outputs 中逐段登记；一段多次改写时追加事件，关联旧 ID。block ID 在稿件版本间稳定；不同文段使用不同 ID。行号会移动，不作为唯一定位方式。

target.path 是稿件目标位置。target.git_commit 尚未提交时为 null，之后通过新的 handoff 事件绑定真实提交，不回填一个不存在的未来提交，也不静默修改原生成事件。核对历史稿件时读取对应提交；当前稿件后来改写，不改变原始输出快照的内容。

passage_revised 保存改写后的快照及目标文段，必须关联原事件。没有调用 subagent 的仓库初始化记录使用 work/verification，不伪造 passage_generated。

## 提示词与校验值

提示词快照保存到已有 A 记录目录的 input.md，必须包含实际填充的公共说明、阶段模板、材料版本、限制与本轮指令，不能只写“使用模板E”。

原始输出 output.md 保留稳定标记与原文；可编辑稿件放正文目录。已用于日志的提示词、输出快照不覆盖，修订另建记录或固定 Git 提交。

文本文件的 hash_mode=sha256_utf8_lf：UTF-8 内容将 CRLF/CR 统一为 LF 后计算 SHA256，保留其他空白与结尾换行。二进制使用 sha256_bytes。文段 hash 只计算开始标记后的换行到结束标记前换行之间的文本，内文空白保持不变。

git_commit 非 null 时按该提交读取文件；否则读取实际工作区文件。工作输出若是会继续修改的普通文档，先记录产出路径，提交后用 handoff 事件绑定提交与校验值；不要把可变工作文件当作不可变快照。

受限资料可以使用 local_only，路径仍为相对仓库的 .local/...；核对完整证据时需合法取得这些文件。缺少证据时只描述元信息，不得称内容已核验。

## 当前搭建范围

当前只保存标准 schema、字段说明和记录示例，不实现校验器、不编写测试、不安装开发工具依赖。后续需要自动记录或实际代码验证时，再根据作者要求增加相应实现。

[示例事件](templates/examples/passage-generated.example.json)明确标记 example，相关 prompt.md 与 output.md 是演示资料，未调用 subagent、不属于书稿。初始化阶段没有真实文段生成事件。第一周正式提纲任务实际调用的subagent另记于各章ai-records及当日JSONL，不能与示例混用。

多个 subagent 共同形成同一文段时，分别保存生成事件，由整合或改写事件关联全部来源；不要将多人结果登记为一个虚构的 agent。
