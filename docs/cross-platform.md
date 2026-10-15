# 本地环境与可移植性

当前MNIST结构分析和PyTorch到ONNX导出使用本地PC的CPU即可完成，不依赖GPU。

## 基本环境

记录与复现直接相关的版本：

- Python；
- PyTorch；
- torchvision；
- ONNX；
- 执行导出检查时实际使用的其他包。

支持范围应根据PyTorch、torchvision与ONNX官方兼容关系及实际目标工具要求给出，不把一次安装版本写成唯一可用版本。

## 路径与产物

代码使用仓库相对路径和`pathlib`，不硬编码Windows盘符。MNIST数据放`02-onnx-baseline/data/`，权重放`02-onnx-baseline/model/`，ONNX和检查输出放`02-onnx-baseline/outputs/`；这些目录由Git忽略。

导出前显式设置评估模式并确保模型与样例输入位于同一设备。权重加载优先映射到CPU。opset、动态维度和算子支持必须与目标部署工具的对应版本核对，PC端导出成功不等于目标硬件可部署。
