# 环境与兼容性记录

| 环境角色 | 系统 | 设备 | 框架与驱动版本 | 当前证据 |
| --- | --- | --- | --- | --- |
| autodl-train | AutoDL Linux，具体发行版待登记 | GPU型号/显存/CPU/内存待登记 | Python/PyTorch/torchvision/CUDA/驱动待安装核验 | 作者指定的训练环境，尚未运行模型 |
| windows-test | Windows本机，版本待登记 | CPU/内存/摄像头待登记；作者说明使用AMD显卡 | CPU框架/ONNX Runtime待安装核验 | 作者指定的运行测试环境，尚未运行模型 |

两台环境的代码提交、模型与固定输入清单、包版本、实际 device/providers、数值精度和验证 E 记录应一起登记。模型后端不能由“机器上有某种显卡”推断。

本次 JSON 日志校验使用独立开发工具依赖 requirements-dev.txt，不是上述训练环境的兼容性证明。
