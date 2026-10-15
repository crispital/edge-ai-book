# S02-黄章磊-001 · 官方MNIST基准

机构：PyTorch。实际阅读日期：2026-10-15。
来源：[官方目录](https://github.com/pytorch/examples/tree/main/mnist)。
固定提交：acc295dc7b90714f1bf47f06004fc19a7fe235c4，由GitHub API查询main取得；实际打开[固定版本源码](https://github.com/pytorch/examples/blob/acc295dc7b90714f1bf47f06004fc19a7fe235c4/mnist/main.py)。
实际阅读：main.py全文件、README、requirements.txt及仓库LICENSE。源码静态阅读，未运行；原文件未保存本地，SHA256未生成，可由固定链接取得。作者核对待完成。此版本用于查阅定位，团队训练/导出最终使用的提交需对齐。

## 可确认的边界
- Net的forward返回log_softmax；test使用eval和no_grad，并以argmax取类别。结果比较应使用相同语义。
- 示例前处理为ToTensor后Normalize，均值0.1307、标准差0.3081；本地接入须与前序保持一致。
- 示例支持训练、测试和保存state_dict，没有ONNX导出或ONNX Runtime实现。
- requirements仅列torch、torchvision，未锁定版本；不能据此声称当前环境兼容。

位置：Net及forward约9—31行，test约49—64行，前处理约107—114行，保存权重约126—127行。
用途：2.8输入/输出一致性；2.9来源及语义；4.1模型对象。实际ONNX名称、shape、opset、文件大小和性能需模型交付及运行才能确认。

项目源码许可证为仓库BSD-3-Clause，后续复制或改编代码时保留版权、条款及免责声明。MNIST数据的分发条件需单独核对，不能把代码许可套给数据。当前仅建立来源记录，未复制上游代码。
