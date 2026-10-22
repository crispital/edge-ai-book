# MNIST模型结构与ONNX导出

本项目服务2.6和2.7：先读懂MNIST PyTorch模型的结构与张量形状，再导出ONNX并检查结构、接口和数值。

作者指定的模型源码已原样保存为[src/main.py](src/main.py)，读取位置、SHA256和静态说明见[M02-001](../docs/references/ch02/notes/MNIST项目源码.md)。本次仅复制源码。运行该脚本会进入训练流程；指定`--save-model`才保存权重，使用`--no-accel`选择CPU。

## 目录

- `src/`：模型定义与可复用代码；
- `scripts/`：导出、结构检查和数值对比入口；
- `docs/`：模型版本、导出参数和限制；
- `samples/`：许可明确的固定小样例或样本清单；
- `data/`：本地MNIST数据；
- `model/`：本地PyTorch权重；
- `outputs/`：本地ONNX及检查输出。

后三个目录不进入Git。
2026-10-22起，按作者明确授权，固定复现文件作为例外纳入当前交付分支：四个完整MNIST IDX文件、原权重、原始ONNX和已有10样本回归输出。仅放行清单文件，其他运行产物继续忽略；大小、来源及SHA256见[复现文件清单](docs/reproduction-files.json)。上句“不进入Git”是原始通用规则，本次例外以本段为准，历史实验报告不追改。

取得本分支后，数据已位于`data/MNIST/raw/`，不需要重新下载或训练即可执行原模型数值对比。在仓库根目录运行，使用已安装对应依赖的Python：

```powershell
python -B 02-onnx-baseline/scripts/compare_outputs.py --output-dir 02-onnx-baseline/outputs/regression_local
```

输出目录必须是尚不存在的新目录；已有ONNX无需重复导出。数据沿用原工程中的MNIST文件，未改动样本、标签或划分；来源说明见[MNIST资料卡](../docs/references/ch02/notes/MNIST基准.md)。

作者提供的权重已保存为本地`model/mnist_cnn.pt`；来源、文件校验值和源码匹配结果见[模型版本记录](docs/model-version.md)。

## 2.6产出

- 实际模型的结构或计算图；
- Conv、激活、池化、Flatten、Gemm等算子与形状对照；
- 输入输出、权重、静态/动态维度和布局说明。

## 2.7产出

- 导出与检查脚本；
- 评估模式、样例输入、输入输出命名、固定或动态形状设置；
- opset及目标工具支持依据；
- 原始ONNX、派生版本及重新验证记录；
- PyTorch与ONNX的同输入数值对比；
- 模型版本记录。

训练过程由前序小节负责。本项目不把PC端导出成功直接解释为目标硬件兼容。

## 运行ONNX导出

脚本：[scripts/export_onnx.py](scripts/export_onnx.py)。采用PyTorch的torch.export导出路径（dynamo=True），本次已核对本地PyTorch 2.14.1+cpu的API。该接口需要onnx和onnxscript；当前虚拟环境已有onnx，可在PowerShell中执行：

```powershell
& F:\edge-ai-book\.env\Scripts\python.exe -m pip install onnxscript
cd F:\edge-ai-book\d2el\02-onnx-baseline
& F:\edge-ai-book\.env\Scripts\python.exe -B scripts\export_onnx.py
```

脚本按自身位置查找model/mnist_cnn.pt，加载Net、切换eval、构造float32固定输入[1,1,28,28]，导出到outputs/mnist_cnn.onnx并执行ONNX checker。输入名称为input，输出名称为log_probs，输出语义沿用源码的10类对数概率。样例中的零张量只用于图导出，不是准确率测试样本。

省略--opset时采用当前导出器推荐值，运行后打印文件实际opset及输入输出信息。指定目标工具支持版本时使用--opset参数；已有输出文件不会覆盖，可通过--output另存：

```powershell
& F:\edge-ai-book\.env\Scripts\python.exe -B scripts\export_onnx.py --output outputs\mnist_cnn_v2.onnx
```

本脚本不设置动态维度，不调用外部简化工具。关闭导出器可选optimize步骤不代表导出过程完全没有图变换。作者已经导出本地`outputs/mnist_cnn.onnx`；该文件已经重新读取并通过ONNX checker，实际使用opset 20，输入为float32的`[1,1,28,28]`，输出为float32的`[1,10]`。文件校验值和读取记录见[模型版本记录M02-003](docs/model-version.md)。这与早期仅检查脚本语法及`--help`入口的记录属于不同工作阶段。

结构检查不能替代同输入数值回归。以上导出命令供复现使用，已有文件时应通过`--output`指定新文件名。

## 运行导出数值回归

[scripts/compare_outputs.py](scripts/compare_outputs.py)只检查导出前后的数值一致性，不训练、不导出、不修改现有模型。默认从工程data目录读取已存在的MNIST测试集，不自动下载；也可用--data-dir指定已有数据目录。前处理与src/main.py一致，固定使用测试集索引0—9、CPU float32和逐张输入。

本次实际执行命令如下，从仓库根目录运行；终端若出现中文乱码，可在-B前另加-X utf8，不改变计算：

```powershell
& F:\edge-ai-book\.env\Scripts\python.exe -B `
  02-onnx-baseline\scripts\compare_outputs.py `
  --data-dir F:\edge-ai-book\02-onnx-baseline\data `
  --output-dir 02-onnx-baseline\outputs\regression_20261016_01
```

脚本不覆盖已有输出目录。复现时将--output-dir改为新目录，或在工程目录运行时使用outputs下的新路径。若数据已经放在工程data目录，可省略--data-dir。

输出目录保存outputs.npz（输入、标签、索引、两侧原始输出）和summary.json（逐样本类别、误差和总体判定）。NPZ中的inputs为[10,1,28,28]，表示10份归档样本；模型实际仍逐张接收[1,1,28,28]，不表示ONNX具有动态批次。

绝对容差1e-5、相对容差1e-4在执行前固定，只作为本次教学实验判据。10张样本均满足联合容差，类别全部一致；最大绝对误差约5.72e-6，非零参考值上的最大相对误差约2.38%。相对误差较大的一项参考值接近零，解释及完整记录见[实验报告](../reports/ch02/E02-07-20261016-01/README.md)。超出容差时脚本先保存结果再以退出码1结束；形状错误或非有限值直接报错，不产生有效对比结论。
