# d2el ·《端侧人工智能》个人写作与开发仓库

黄章磊负责的第一阶段工作：3.1 从 MNIST 到真实业务任务、3.2 自有 RGB 图像数据与迁移学习、3.3 任务评价指标与业务指标、4.1 为什么需要轻量化。

本仓库用于保存书稿、代码、资料索引和可追溯的工作记录。当前已形成第一周设计材料：四节提纲、图表/代码需求清单和README框架，尚未实现训练、推理或评测功能。

## 从这里开始

- [第一周交付材料](docs/first-week-2026-10-11.md)：按3.1、3.2、3.3、4.1阅读并审查提纲与清单。
- [开发者 HTML 导览](docs/developer-guide.html)：目录地图、功能安排、跨平台分工与记录去向，可离线打开。
- [个人工作 SPEC](第一阶段/docs/SPEC.md)
- [文档与记录入口](docs/README.md)
- [目录、上传范围与扩展规则](docs/repository-layout.md)
- [提交和分支规范](CONTRIBUTING.md)
- [Agent 入口规则](AGENTS.md)
- [迁移学习项目 README 框架](03-transfer-learning/README.md)
- [模型基线项目 README 框架](04-lightweight/README.md)
- [本次初始化日志](docs/logs/2026/10/2026-10-11.md)
- [JSON日志schema与文段溯源](docs/logging-schema.md)
- [AutoDL Linux训练与Windows CPU测试](docs/cross-platform.md)

## 开发入口

代码项目沿用分工计划目录，不在“第一阶段”下再建一套代码：
- `03-transfer-learning/`：自有 RGB 分类、迁移学习、导出与摄像头验证。
- `04-lightweight/`：本作者的 4.1 模型基线及资源预算说明；其余压缩方法由相应作者负责。
- `docs/`：正文、提示词、任务与资料记录。
- `assets/`：图表及可编辑源文件。
- `reports/`：实验计划、正式报告及可共享证据。
- `datasets/`、`compatibility/`、`common/`：数据说明、验证过的版本记录、实际复用代码。

模型与完整数据不直接入库，按项目说明保存到本地 `.local/`，通过清单、版本、校验值和合法获取方式交接。

## 仓库状态

GitHub：<https://github.com/dixiLOG/d2el>。个人工作分支采用 `feature/章号-节号-姓名`。初始化使用 `feature/03-02-黄章磊`；第一周设计工作从其已提交框架创建`feature/03-01-黄章磊`。提纲不表示小节或项目已完成。

仓库尚无经过审核的稳定版本，暂不创建 `main`、`develop` 或阶段发布标签。后续接入团队 Gitee 时保留 `origin`，按 [提交规范](CONTRIBUTING.md) 添加 `upstream`，不覆盖任一远端历史。
