# 仓库结构与上传范围

```text
edge-ai-book/
├── 第一阶段/docs/SPEC.md
├── 02-onnx-baseline/
│   ├── src/          模型与可复用实现
│   ├── scripts/      导出和检查入口
│   ├── docs/         模型版本与接口说明
│   └── samples/      可共享的小样例或清单
├── docs/
│   ├── ch02/         2.6、2.7提纲与正文
│   ├── references/ch02/
│   └── logs/
├── assets/ch02/      图表及可编辑源文件
├── reports/ch02/     实验计划、报告与可共享证据
├── datasets/         数据来源与清单说明
├── compatibility/    环境版本记录
└── common/           出现真实复用需求后提取的公共代码
```

完整数据、权重、ONNX、运行输出、缓存、虚拟环境和本机配置由`.gitignore`排除。仓库相对路径使用正斜线；代码不硬编码盘符或用户目录。

当前仓库独立维护，唯一远程为`https://github.com/crispital/edge-ai-book.git`。原克隆仓库不作为upstream，也不参与后续合并流程。
