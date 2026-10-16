# MNIST模型版本记录

## M02-002 · 作者提供的权重

- 读取与复制日期：2026-10-15。
- 来源：作者指定的`F:/edge-ai-book/02-onnx-baseline/model/mnist_cnn.pt`。
- 本地副本：`02-onnx-baseline/model/mnist_cnn.pt`，已保存，受Git忽略规则保护。
- 文件大小：4,803,113字节。
- 原文件与副本字节SHA256：`9d23854dcf95327f9996bcd583909b2778a6c475372cd79ab36ca54d26ccbf64`，两者一致。
- 对应源码：[src/main.py](../src/main.py)；源码来源及校验值见[M02-001](../../docs/references/ch02/notes/MNIST项目源码.md)。

## 实际读取与匹配检查

执行环境：Python 3.13.9，PyTorch 2.14.1+cpu。该环境版本来自本次实际读取，不是支持范围声明。

使用`torch.load(path, map_location="cpu", weights_only=True)`读取副本，得到OrderedDict；使用`Net().load_state_dict(state, strict=True)`检查，输出为`All keys matched successfully`。

实际读取的8个张量均为torch.float32：

| 名称 | shape |
| --- | --- |
| conv1.weight | [32, 1, 3, 3] |
| conv1.bias | [32] |
| conv2.weight | [64, 32, 3, 3] |
| conv2.bias | [64] |
| fc1.weight | [128, 9216] |
| fc1.bias | [128] |
| fc2.weight | [10, 128] |
| fc2.bias | [10] |

## 适用范围与记录边界

该权重可作为2.6结构分析和2.7导出准备的本地输入。严格加载确认了键名和张量结构匹配，不证明它由某次特定训练产生，也不证明准确率。

文件只包含本次读取到的参数字典，没有训练轮数、优化器状态或训练日志；不能从源码默认参数反推训练条件。本次没有执行前向推理、准确率评估、ONNX导出或数值回归。4.5仍需第三章RGB模型。

Git仅保存本记录；不提交权重副本。

## M02-003 · 作者导出的原始ONNX

读取与检查日期：2026-10-15。作者报告已完成导出，本次实际读取文件并重新执行结构检查；本次未重新导出。

- 本地位置：`02-onnx-baseline/outputs/mnist_cnn.onnx`。
- 文件大小：4,810,666字节。
- 字节SHA256：`1601b8478b865ae40acfdf4c727cccb298f463a5ff754931112277e658a8b3c7`。
- 实际读取位置：ModelProto.ir_version、producer_name、producer_version、opset_import；graph.input、graph.output、graph.node、graph.initializer。
- 文件记录的导出器：pytorch，2.14.1+cpu；IR版本10；ai.onnx opset 20。
- 本次检查库：ONNX 1.23.2；`onnx.checker.check_model`通过。
- 输入：input，FLOAT（float32），固定shape [1,1,28,28]。
- 输出：log_probs，FLOAT（float32），固定shape [1,10]；末端为LogSoftmax。
- 主图节点数：13；主图initializer没有标记外部数据。

实际算子数量：Conv×2、Relu×3、MaxPool×1、Constant×2、Concat×1、Reshape×1、Gemm×2、LogSoftmax×1。

本图没有Flatten节点，源码展平操作对应Reshape及形状相关节点；没有Dropout节点。2.6的实际算子表应记录这一结果，不将源码层名直接当成ONNX节点名。

此检查确认了结构合法性及实际接口，没有执行同输入PyTorch/ONNX数值回归或准确率评估。opset 20是本文件属性，不是目标芯片SDK兼容结论。ONNX文件由Git忽略。

## M02-004 · 原始ONNX的同输入数值回归

执行日期：2026-10-16，Codex在作者确认方案后实际运行；不重新训练、不重新导出。使用M02-002权重与M02-003原始ONNX，文件SHA256保持不变。

- 脚本：[scripts/compare_outputs.py](../scripts/compare_outputs.py)。
- 实验ID：E02-07-20261016-01；[完整输入版本、运行命令、结果与校验值](../../reports/ch02/E02-07-20261016-01/README.md)。
- Python 3.13.9、PyTorch 2.14.1+cpu、torchvision 0.29.1+cpu、NumPy 2.5.4、ONNX Runtime 1.31.0；执行后端CPUExecutionProvider。
- MNIST测试集索引0—9；ToTensor及Normalize((0.1307,), (0.3081,))；float32 NCHW，每次输入[1,1,28,28]。
- 运行前判据：atol=1e-5、rtol=1e-4；逐元素abs(onnx-reference) <= atol + rtol * abs(reference)。
- 实际结果：10份样本共100个输出值全部满足判据，两侧类别10/10一致；最大绝对误差5.7220458984375e-6，非零参考值上的最大相对误差0.02380949353407169。
- 参考值为零的元素1个，该位置ONNX也为零；相对误差不计此位置。
- 实际保存：本地outputs/regression_20261016_01/outputs.npz与summary.json，由Git忽略。

该结论限于本次10份固定样本和容差，不是完整测试集准确率，不证明具体硬件或SDK兼容。前述M02-002、M02-003的“本次未执行”属于各自历史检查范围，不代表当前仍没有数值回归记录。
