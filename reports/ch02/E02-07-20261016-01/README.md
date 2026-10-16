# E02-07-20261016-01 · 导出数值回归

## 运行前方案

作者已确认执行。比较现有PyTorch权重与原始ONNX，不训练、不重新导出、不简化模型。

- 模型：工程src/main.py的Net；权重model/mnist_cnn.pt；ONNX为outputs/mnist_cnn.onnx。
- 样本：本地MNIST测试集索引0—9，不随机抽样，不自动下载。
- 前处理：ToTensor后按均值0.1307、标准差0.3081归一化，与原源码一致。
- 输入：CPU float32、NCHW；ONNX固定batch=1，因此逐张执行。
- 参考：PyTorch eval及inference_mode；ONNX Runtime显式使用CPUExecutionProvider。
- 预先固定判据：每个输出元素满足abs(onnx-reference) <= 1e-5 + 1e-4 * abs(reference)，全部元素满足才通过；形状相同且数值有限是前置要求。
- 同时报告预测类别、最大绝对误差、非零参考元素上的最大相对误差；零参考元素不计算相对误差，单独计数。
- 保存：输入、标签、样本索引、两侧原始输出、逐样本类别及误差；本地outputs/regression_20261016_01/，不覆盖已有目录。
- 结论范围：仅这10张样本和本次容差，不代表全测试集准确率或目标硬件兼容性。

## 实际执行

上面的计划先于真实样本执行保存；以下结果在运行后追加。

## 实际执行结果

执行日期2026-10-16；执行者Codex，作者已确认实验方案。运行时工作基线为main分支、提交288840aa6e60c63439c90e20e1fc34d14ed6cb47，存在未提交改动；具体实现以本次脚本SHA256为准，不能把该提交当作包含本次脚本的版本。

实际命令（仓库根目录）：

```powershell
& F:\edge-ai-book\.env\Scripts\python.exe -B `
  02-onnx-baseline\scripts\compare_outputs.py `
  --data-dir F:\edge-ai-book\02-onnx-baseline\data `
  --output-dir 02-onnx-baseline\outputs\regression_20261016_01
```

真实进程退出码0。Python 3.13.9、PyTorch 2.14.1+cpu、torchvision 0.29.1+cpu、NumPy 2.5.4、ONNX 1.23.2、ONNX Runtime 1.31.0；显式选择CPUExecutionProvider。原ONNX来自M02-003，opset 20、IR 10；本次没有修改导出参数或重新导出。

10张图片、100个float32输出值均有限且满足预先固定的联合容差，两侧类别10/10一致。这里只比较样本结果，不将其称为完整MNIST准确率。

| 测试集索引 | 标签 | PyTorch类别 | ONNX类别 | 最大绝对误差 | 非零参考最大相对误差 | 满足联合容差 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 7 | 7 | 7 | 5.722046e-6 | 2.015305e-7 | 是 |
| 1 | 2 | 2 | 2 | 3.814697e-6 | 2.069824e-7 | 是 |
| 2 | 1 | 1 | 1 | 5.722046e-6 | 3.480132e-7 | 是 |
| 3 | 0 | 0 | 0 | 3.814697e-6 | 2.380949e-2 | 是 |
| 4 | 4 | 4 | 4 | 1.907349e-6 | 9.917922e-8 | 是 |
| 5 | 1 | 1 | 1 | 1.907349e-6 | 1.246574e-7 | 是 |
| 6 | 4 | 4 | 4 | 1.907349e-6 | 1.162473e-7 | 是 |
| 7 | 9 | 9 | 9 | 1.907349e-6 | 1.887960e-7 | 是 |
| 8 | 5 | 5 | 5 | 3.814697e-6 | 3.302766e-7 | 是 |
| 9 | 9 | 9 | 9 | 3.814697e-6 | 1.708957e-7 | 是 |

总体最大绝对误差为5.7220458984375e-6，非零参考值上的最大相对误差为0.02380949353407169。最大相对误差来自索引3、输出类别0：参考值-5.006777428206988e-6，ONNX值-5.125986263010418e-6，绝对差异1.1920883480343036e-7。比例约2.38%来自参考值接近零，绝对差异仍小于atol=1e-5。参考值为零的元素共1个，ONNX在该位置同样为零；不以任意epsilon替代零分母。

误差使用已保存float32输出转float64后计算，不改变推理精度。类别一致与逐元素数值通过分别报告，不能相互替代。

## 文件与版本

以下为实际读取的文件字节SHA256。原始数据完整文件、权重、ONNX及数值输出仅本地保存，不进入Git。

| 工程相对位置 | 字节数 | SHA256 |
| --- | --- | --- |
| src/main.py | 5809 | 666d7428386b77b93d0055fb2a11118f2c350324dc410e54d072c791e062bb5c |
| scripts/export_onnx.py | 3596 | 40881d291f51ab60b3d55b5c2ec90bed64c2e6f9d8edeeec5f7f8a68904574b7 |
| scripts/compare_outputs.py | 4882 | fe87841238013e726d3992a67163795eacc1a04a2b12102639bb1d88efda1c96 |
| model/mnist_cnn.pt | 4803113 | 9d23854dcf95327f9996bcd583909b2778a6c475372cd79ab36ca54d26ccbf64 |
| outputs/mnist_cnn.onnx | 4810666 | 1601b8478b865ae40acfdf4c727cccb298f463a5ff754931112277e658a8b3c7 |
| outputs/regression_20261016_01/outputs.npz | 4944 | a422d7c022e69d95679613dc08a51db7868d670af6b9f0034721f43973a2b56f |
| outputs/regression_20261016_01/summary.json | 2800 | 3b01366d9ebed984f8a69b3b08769775e37790b631db476df3ab2132c5fcdb91 |

输入数据实际读取自作者原工程F:/edge-ai-book/02-onnx-baseline/data/MNIST/raw/，使用download=False，不下载、不移动数据：

- t10k-images-idx3-ubyte：SHA256为0fa7898d509279e482958e8ce81c8e77db3f2f8254e26661ceb7762c4d494ce7
- t10k-labels-idx1-ubyte：SHA256为ff7bcfd416de33731a308c3f266cc351222c34898ecbeaf847f06e48f7ec33f2

outputs.npz中inputs形状[10,1,28,28]、float32；labels和indices均为[10]、int64；pytorch与onnx均为[10,10]、float32。归档批次维是10，不代表模型接受batch=10。所有原始输出均已保存，并非只保留argmax或统计摘要。

## 依据表

| 陈述或条目 | 来源ID或记录ID | 实际读取片段位置 | 适用版本 | 核对结果 |
| --- | --- | --- | --- | --- |
| 模型结构及前处理相同 | M02-001 | src/main.py的Net、forward及第124—125行 | 本报告源码SHA256 | 已实际读取并用于执行 |
| 使用作者原权重及原始ONNX | M02-002、M02-003 | 文件SHA256、严格加载、Session输入输出元信息 | 本报告文件SHA256、opset 20 | 本次实际读取，未更换 |
| 10张样本通过联合容差，类别一致 | E02-07-20261016-01、M02-004 | outputs.npz的inputs/pytorch/onnx及summary.json.samples | 本次CPU依赖版本 | 已实际运行并保存 |
| 相对误差放大与零值规则 | 同上 | 输出[3,0]、reference==0位置及compare函数 | 本次100个输出值 | 已实际定位原始输出 |
| 初学者正文保留核心代码与真实条件 | P01-001 | 原PDF52页全文；印刷第20、44页 | 2020年指南 | 本轮实际重读，未作出版社审核 |

## 检查与边界

临时直接检查误差计算的7个情形：相同数组、可手算的超差、纯零参考、类别不变但数值超差、形状不匹配、NaN、无穷大。实际均通过预期行为检查；没有新增永久测试目录。初次“脚本尚不存在”的失败仅是入口存在性检查，不把它当作数值算法的严格TDD失败证据。

另从已保存outputs.npz重放10份输入，重新执行PyTorch与ONNX，结果分别与归档原始输出逐元素完全一致；重新计算总体误差与summary.json一致。CLI --help及AST语法检查通过；向已有输出目录运行时按预期返回退出码2，原outputs.npz的SHA256保持不变。Git忽略检查确认两份数值输出不进入版本控制。

未执行全测试集准确率、简化模型、动态形状或板端验证。没有测量性能，不填写性能数字；运行结果不等于作者试读或外部审核。未提交或推送。
