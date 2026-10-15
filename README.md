# d2el ·《端侧人工智能》个人写作与开发仓库

黄章磊第一阶段当前负责 **2.8 ONNX Runtime基线推理、2.9 面向硬件部署的模型接口、4.1 为什么需要轻量化**。2026-10-15调整任务，统一使用[PyTorch官方MNIST示例](https://github.com/pytorch/examples/tree/main/mnist)。

## 从这里开始
- [个人SPEC](第一阶段/docs/SPEC.md)：当前范围与配套产出。
- [当前任务与材料](docs/current-tasks.md)：提纲、任务卡及待办。
- [开发者HTML导览](docs/developer-guide.html)：离线目录地图。
- [文档入口](docs/README.md)、[目录规则](docs/repository-layout.md)、[提交规则](CONTRIBUTING.md)、[Agent规则](AGENTS.md)。
- [ONNX基线项目](02-onnx-baseline/README.md)、[轻量化动机与基线](04-lightweight/README.md)。
- [工作日志与卡片](docs/records.md)、[文段溯源](docs/logging-schema.md)、[跨平台要求](docs/cross-platform.md)。

当前是任务设计与工程骨架，未训练模型、导出ONNX或运行推理。前序训练和2.7导出由对应作者提供，本人承接验证与接口整理。

代码放对应项目，文档放docs，图表放assets，实验放reports；完整数据与权重放.local，通过来源、版本、清单与校验值交接。开发框架不随本次任务调整重建。

## 历史与仓库
[2026-10-11第一周材料](docs/first-week-2026-10-11.md)及原AI快照保留为历史。根目录SPEC/原团队资料暂未更新，以个人SPEC为当前依据。

仓库：[dixiLOG/d2el](https://github.com/dixiLOG/d2el)。本次范围修改仍在已有分支进行；新任务分支命名见CONTRIBUTING，不自动重命名远端或更改默认分支。尚无团队审核后的稳定版本。
