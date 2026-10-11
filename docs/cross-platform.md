# Linux 训练与 Windows 测试

本项目当前采用作者指定的两台环境：AutoDL Linux 开发与训练，Windows 本地主机运行链路、摄像头及 PC 基线测试。本节是后续实现约束，尚未证明模型已在任一环境运行。

## 环境角色

作者指定Linux训练、Windows运行测试及CPU/GPU兼容需求。CPU基线、float32参考、pathlib、workers=0和交接清单是本仓库实现约定，不是指南指定；引用技术文档的版本不代表项目已选择该依赖版本。

| 环境 | 用途 | 设备策略 |
| --- | --- | --- |
| AutoDL Linux | 数据与模型开发、迁移学习、导出、训练侧验证 | 如实际实例为 NVIDIA GPU，显式配置 cuda:0；型号、驱动与 CUDA 构建版本需实际登记 |
| Windows 本地主机 | 固定输入对照、CPU 推理、摄像头链路、PC CPU 耗时 | 显式配置 cpu，ONNX Runtime 使用 CPUExecutionProvider |
| Linux CPU | 可选的功能检查路径 | 显式配置 cpu；不把功能验证当作 GPU 性能验证 |

AMD 显卡不是 Windows 测试的必需依赖。若以后启用其加速后端，应作为另一个配置和验证范围，不能悄悄改变当前 CPU 基线。

配置示例在：
- [Linux AutoDL 训练](../03-transfer-learning/configs/linux-autodl-train.example.json)
- [Windows CPU 测试](../03-transfer-learning/configs/windows-cpu-test.example.json)
- [Windows CPU 基线](../04-lightweight/configs/windows-cpu-baseline.example.json)

这些文件只是配置结构示例，尚无程序读取它们执行训练或测试。业务类别、学习率、训练轮次、输入尺寸及实验阈值不在初始化中填入。

## 路径与代码

共享清单一律使用仓库相对路径、正斜线和 UTF-8；大小写精确匹配，不能依赖 Windows 的大小写宽容。代码通过 pathlib 处理文件路径，明确以仓库根或配置基准解析；不依赖进程启动目录。

两台机器的完整数据、模型、日志分别保存到各自 .local。共享配置不能包含 Windows 盘符、AutoDL 实例绝对路径、账号或 IP；本机覆盖参数用 CLI 或 .local 中的本地配置。不要复制 Windows venv、Linux 二进制或整套环境文件夹。

核心步骤用 Python 入口，避免核心逻辑只存在于 Bash/PowerShell。需要 shell 包装时分别说明 Linux 与 PowerShell 命令。Linux 文件名大小写、Windows spawn 多进程和摄像头设备选择都应进入实际验证。

Windows 可执行入口使用 if __name__ == "__main__" 保护。DataLoader 的 dataset/collate/worker 函数应为可导入的顶层定义；跨平台最小路径从 num_workers=0 开始，之后按实测增加。这些约束对应 [PyTorch 多进程加载说明](https://docs.pytorch.org/docs/2.14/data.html#platform-specific-behaviors)。

## CPU/GPU 设备

模型及输入张量使用同一个明确设备，不在核心代码中硬编码 .cuda()。显式请求 CUDA 时先检查可用性，不可用则报错；功能演示若允许自动回退，必须明确标为非基准测试并记录实际设备，不能默默转 CPU 后仍标 GPU 结果。

训练交接保存模型 state_dict，并记录架构、类别数及训练版本；加载时先映射 CPU，再移到请求设备，避免 Windows 本机需要训练时的 CUDA 设备。该映射由 [torch.load 的 map_location 参数](https://docs.pytorch.org/docs/2.14/generated/torch.load.html)支持。恢复训练的优化器状态作为训练检查点另存，不能替代交接模型。

Windows CPU ONNX 测试显式指定 CPUExecutionProvider；GPU 侧如需 ONNX 验证，单独配置并记录可用与实际 providers。providers 的优先级及算子回退按 [ONNX Runtime API](https://onnxruntime.ai/docs/api/python/api_summary.html)处理，不把“GPU provider 出现在列表”视为所有计算都在 GPU。

先建立 float32 参考路径；混合精度、量化或其他后端各自记录配置及误差，不要求所有训练运行逐位一致。固定模型与输入的跨后端对照应预先规定检查方法和允许误差，不自行填写阈值。

## 跨机模型交接

从训练机器交给 Windows 的包至少包含：
- 权重、ONNX 及实际存在的 ONNX 外部数据文件，逐文件 SHA256。
- 模型架构与预训练来源、类别表及类别顺序。
- 输入输出名称、形状、dtype、颜色、布局、Resize/裁剪/归一化、后处理。
- 固定测试样本清单及可获得的文件，参考输出及其实际生成环境。
- 训练与导出 Git 提交、数据划分版本、工具版本、模型信息卡和关联实验 ID。
- 合法获取与存放方式；未验证、失败及限制。

只移动结果包与元信息，不移动 .local 私人配置。接收机器先核对校验值、类别和前后处理，再运行固定输入对照，最后接摄像头。若接口或类别变化，重新验证受影响步骤。

## 环境与依赖记录

两台机器分别建立环境，不使用同一个未经验证的 CUDA 安装指令。训练环境与 CPU 环境的依赖入口分开；共同包版本尽量保持一致，PyTorch 构建和 CUDA 运行依赖按角色选择。

具体版本在实际安装与最小运行验证后锁定；初始化不假设 AutoDL 镜像或 Windows PyTorch 可用版本。不得将一台机器的 pip freeze 原样当作另一平台的通用 requirements。实际进度见 [环境矩阵](../compatibility/environment-matrix.md)。

## 验证边界

先分别检查 Windows CPU 和 Linux 训练侧最小路径，再执行同一交接包的固定输入对照。GPU 计时注意异步计算与同步点；CPU 记录线程、预热、重复次数及计时范围。摄像头采集、前处理、模型、后处理和显示分开记录。

当前框架与配置示例不证明链路已运行；后续训练、CPU 推理和摄像头运行情况另存实际 E 记录。
