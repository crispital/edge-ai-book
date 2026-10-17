# 2.7 PyTorch模型导出ONNX：提纲及资料任务

来源详情见[本节独立资料卡](../../references/ch02/notes/02-07-资料卡.md)，包含版本、实际读取位置和保存情况。

## 本节任务

本节建立完整的导出验收流程：准备模型和样例输入，定义接口，选择与目标工具匹配的opset和形状策略，导出ONNX，再检查结构、接口和数值一致性。

读者需要能够加载PyTorch模型和权重，理解评估模式，并能构造符合接口要求的张量。模型训练由2.1—2.4负责，ONNX基础由2.5负责，完整ONNX Runtime基线教程由2.8负责。

## 提纲

1. 文件生成了，为什么仍不能直接认为导出成功
2. 导出前确认模型定义、权重来源和评估模式
3. 准备固定样例输入，确定输入输出名称、shape、dtype和layout
4. 根据PyTorch版本选择导出接口
5. 根据目标编译器或运行时证据选择opset
6. 固定shape与动态batch的取舍，以及`dynamic_shapes`或`dynamic_axes`的版本差异
7. 保存原始ONNX并使用ONNX checker检查结构
8. 核对图输入、输出、opset、节点、initializer和shape信息
9. 使用同一输入比较PyTorch与ONNX输出、预测类别和数值误差
10. 区分原始ONNX与简化等派生版本，派生后重新执行检查和回归
11. 边界：导出检查通过不等于目标工具转换或板端部署通过

## 资料搜集问题

1. 项目实际采用的PyTorch、ONNX和导出器版本是什么？
2. 模型真实的输入输出名称、shape、dtype和layout是什么？
3. 目标工具支持哪些opset、算子和动态维度形式？
4. 数值回归使用什么执行后端、误差指标和判定条件？
5. 是否使用模型简化工具；若使用，其版本、变换内容和复验步骤是什么？

## 配套产出计划

- 导出与结构检查脚本；
- 固定输入的数值回归记录；
- 模型版本和接口记录；
- 原始ONNX与派生版本关系表；
- 导出参数表。

## 首批资料入口

- PyTorch 2.14 `torch.onnx.export` API中的样例输入、名称、opset、动态形状和verify参数说明；
- PyTorch官方“Export a PyTorch model to ONNX”教程；
- ONNX Python API Overview中的模型加载、checker和shape inference部分。

## 章级汇总候选

- 知识点：评估模式、样例输入、接口命名、opset、固定与动态维度、模型检查、数值回归、版本派生。
- 小结：ONNX导出不是单一函数调用，而是一套包括接口定义、结构检查和数值回归的验收过程。
- 术语：Example Input、Input Name、Output Name、Numerical Regression、Absolute Error、Relative Error、Derived Model。

## 当前材料缺口

- 作者指定的模型源码、权重和ONNX已保存，见M02-001至M02-003；作者已导出，现有ONNX结构和接口检查记录。固定真实样本、同输入数值回归及原始导出终端全文仍需补充。
- 目标工具版本与支持表尚未提供，不能确定最终opset和动态维度设置。
- 简化工具尚未选定，不能定义具体派生流程。
