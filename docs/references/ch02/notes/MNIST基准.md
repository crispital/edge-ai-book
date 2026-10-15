# S02-001 · PyTorch官方MNIST示例

机构：PyTorch。阅读日期：2026-10-15。

- 官方目录：https://github.com/pytorch/examples/tree/main/mnist
- 固定提交：`acc295dc7b90714f1bf47f06004fc19a7fe235c4`
- 固定源码：https://github.com/pytorch/examples/blob/acc295dc7b90714f1bf47f06004fc19a7fe235c4/mnist/main.py

实际阅读位置：`Net`及`forward`约9—31行，测试函数约49—64行，前处理约107—114行，保存权重约126—127行；同时阅读该目录README、requirements.txt及仓库LICENSE。原网页没有保存到仓库。

## 对2.6和2.7的支持

- `Net`定义可用于说明卷积、池化、展平、全连接和`log_softmax`的结构关系。
- 测试代码使用`eval()`和无梯度上下文，可支持导出前评估模式的解释。
- 前处理为`ToTensor`后按均值0.1307、标准差0.3081归一化，数值回归时应保持一致。
- 示例保存`state_dict`，但不包含ONNX导出、模型简化或目标硬件兼容内容。
- requirements只列torch与torchvision，没有锁定版本，不能由此推出项目的支持版本范围。

PyTorch examples代码使用BSD-3-Clause许可证。MNIST数据的来源与分发条件需独立记录。
