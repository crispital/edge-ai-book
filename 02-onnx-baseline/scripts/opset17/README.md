# opset 17基线配套材料

这些源码和10张固定样本提取自作者提供的2026-11-07发布包，仅统一文本换行并清理一处行末空格，保持代码逻辑与原目录结构，服务2.7已选定的M02-005基线。来源和校验值见[清单](../../../docs/references/ch02/materials-20261111/manifest.json)。

## 文件与运行条件

`02_07_导出与基线推理.py`调用`模型工具.py`，由`official_mnist/main.py`提供Net。样本为MNIST测试集索引0—9的原像素PNG；[来源说明](样例/来源说明.md)记录出处。PyTorch示例源码的BSD许可证附在[LICENSE](official_mnist/LICENSE)。

历史环境为Python 3.11.9、PyTorch 2.4.1、torchvision 0.19.1、NumPy 1.23.5、ONNX 1.17.0、ONNX Runtime 1.20.1。原依赖列表见[requirements-cpu.txt](requirements-cpu.txt)。原导出代码采用该版本的传统导出接口，换用其他PyTorch版本时需要重新核对导出路径。

## 准备模型

把M02-005的两份文件放在本目录下：

- `模型/hzl.pt`，SHA256 `c67f51ea3d3eec2730510d062e5344faf15d9ad5a87537d644dda23438f9a1e7`
- `模型/hzl.onnx`，SHA256 `be5f04249fc79902d79fa12ef4431605f020c961371f83fcb06b41e83483d7d0`

两份模型可从作者的本地迁移包恢复，位置见[跨PC接续说明](../../../docs/ch02/接续说明-20261111.md)。该ONNX为opset 17、动态批次，输入input、输出output，末端为LogSoftmax。

## 使用已有ONNX做比较

在本目录准备上述依赖和模型后执行：

```powershell
python -B -X utf8 -c "from 模型工具 import ROOT,compare; print(compare(ROOT/'模型/hzl.pt',ROOT/'模型/hzl.onnx'))"
```

该入口复用同一组PNG、ToTensor和Normalize(0.1307,0.3081)作为两侧输入，按原容差比较。输出包括预测类别、最大绝对误差和是否通过容差。历史数值及2026-11-10复验见[M02-005](../../docs/model-version.md#m02-005--27正文采用的opset-17基线)。新机器产生的结果另作记录。

## 重新导出

原脚本提供`--output`指定导出目录。使用上述历史环境，从本目录执行：

```powershell
python -B -X utf8 02_07_导出与基线推理.py --output 运行结果/导出推理_新记录
```

选择尚不存在的目录，避免原脚本覆盖同名输出。模型及运行结果目录由Git忽略。

原样保留的样本来源说明提及历史`raw/comparison.json`，该文件未包含在这次可提交材料中；当前10张PNG的字节SHA256见本次清单。样本出版许可仍依原记录的核对状态处理。
