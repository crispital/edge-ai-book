# MNIST ONNX Runtime基线与模型接口

对应个人2.8、2.9。状态：项目骨架及功能清单，尚无可运行推理代码、权重或ONNX；不将官方训练脚本当作已完成的ONNX工程。
依据：[个人SPEC](../第一阶段/docs/SPEC.md)。

## 来源与边界
统一采用[PyTorch官方MNIST示例](https://github.com/pytorch/examples/tree/main/mnist)，查阅提交acc295dc7b90714f1bf47f06004fc19a7fe235c4。来源与限制见[资料笔记](../docs/references/ch02/notes/MNIST基准.md)。
前序章节提供训练权重和PyTorch参考，2.7提供ONNX导出。本人完成Runtime验证和接口文档，不新增训练、导出章节职责。

## 目录
- src/：基线推理和输出对比的实际实现。
- scripts/：实际需要的运行入口，不预定脚本数量。
- configs/：环境配置示例，目前没有程序读取。
- samples/：许可明确的固定小样例或定位清单。
- expected_outputs/：真实参考输出及比较摘要。
- docs/：模型接口模板、MNIST已填写示例和已知限制。
- README.md：环境、运行命令和交接入口。

## 功能与产出
| 功能 | 输入 | 产出 |
| --- | --- | --- |
| 接收基准 | 同版源码、权重、ONNX、固定样本 | 版本与文件清单 |
| Runtime推理 | 与PyTorch一致的输入、评估模式 | Session元信息和原始输出 |
| 数值对比 | 同输入的两端输出 | 类别、绝对/相对误差、判定条件和真实记录 |
| 接口整理 | 代码依据及实际ONNX元信息 | 接口模板和MNIST示例，供4.1及后续平台使用 |

## 环境、命令与预期结果
AutoDL Linux用于前序开发训练；Windows本机以CPUExecutionProvider建立基线，AMD显卡不是必需依赖。详见[跨平台约定](../docs/cross-platform.md)。
Python、PyTorch、torchvision、ONNX与ONNX Runtime版本随前序交付及实际验证确定；官方requirements未锁版本，不能直接称为本项目已验证依赖。
运行命令、依赖文件、固定样本及预期数值在实际实现后补充。当前没有安装、运行或输出一致性结论。

## 交接与限制
权重与完整数据放.local/models及.local/datasets/mnist，文件以清单及SHA256交接。
2.8记录模型、输入、前处理、评估模式、环境、容差和输出；2.9据此整理名称、shape、dtype、layout、类别及后处理。ONNX名称、动态维度和opset须读取真实文件，不能从示例代码猜测。
原始输出为log_softmax结果，对比语义必须保持一致；具体解释见来源笔记。基线不证明任意目标硬件可直接运行。实验记录放reports/ch02。
