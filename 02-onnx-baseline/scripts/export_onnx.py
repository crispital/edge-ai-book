"""将作者的MNIST权重导出为固定形状的ONNX模型。"""

import argparse
import sys
from pathlib import Path

import onnx
import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]  # 根据脚本位置找到工程目录。
sys.path.insert(0, str(PROJECT_ROOT / "src"))       # 让Python找到src/main.py。
from main import Net  # 只导入模型类，不调用main.py中的训练入口。


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--weights", type=Path, default=PROJECT_ROOT / "model" / "mnist_cnn.pt",
        help="PyTorch权重路径",
    )
    parser.add_argument(
        "--output", type=Path, default=PROJECT_ROOT / "outputs" / "mnist_cnn.onnx",
        help="ONNX保存路径；已有文件不会被覆盖",
    )
    parser.add_argument(
        "--opset", type=int, default=None,
        help="目标工具支持的opset；省略时使用导出器推荐值",
    )
    args = parser.parse_args()  # 不传参数时，使用工程内的默认权重和输出路径。
    if args.opset is not None and args.opset < 1:
        parser.error("--opset必须是正整数")
    if not args.weights.is_file():
        parser.error(f"权重文件不存在：{args.weights}")
    if args.output.exists():
        parser.error(f"输出文件已存在，请通过--output指定新文件：{args.output}")

    model = Net().cpu()  # 创建与训练时相同的网络，并放在CPU上。
    state = torch.load(args.weights, map_location="cpu", weights_only=True)  # 读取参数。
    model.load_state_dict(state, strict=True)  # 参数名称、数量和形状必须与网络匹配。
    model.eval()                             # 切换评估模式，使Dropout不再随机丢弃特征。
    example = torch.zeros(1, 1, 28, 28, dtype=torch.float32)  # NCHW：1张、1通道、28×28。

    program = torch.onnx.export(
        model,
        (example,),                  # 单个输入也用元组传入；零张量只示范尺寸和类型。
        input_names=["input"],       # 后续程序用这个名称向模型提供图片张量。
        output_names=["log_probs"],  # 模型输出10类对数概率，而不是原始分数。
        opset_version=args.opset,    # 算子集版本；None表示采用导出器推荐值。
        dynamo=True,                # 使用基于torch.export的ONNX导出器。
        optimize=False,             # 关闭可选图优化，保留初始导出文件供后续对照。
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)  # 输出目录不存在时创建。
    program.save(args.output, external_data=False)        # 网络和权重保存在一个文件中。

    exported = onnx.load(args.output)  # 重新读取保存的文件，检查实际保存结果。
    onnx.checker.check_model(exported)  # 检查结构合法性；不代替数值回归。
    print(f"ONNX结构检查通过：{args.output.resolve()}")
    for item in exported.opset_import:
        print(f"opset：{item.domain or 'ai.onnx'} = {item.version}")
    for label, value in (("输入", exported.graph.input[0]), ("输出", exported.graph.output[0])):
        tensor = value.type.tensor_type                      # 读取张量的类型与形状信息。
        shape = [dim.dim_value for dim in tensor.shape.dim]   # 本脚本导出固定形状。
        dtype = onnx.TensorProto.DataType.Name(tensor.elem_type)
        print(f"{label}：{value.name}，shape={shape}，dtype={dtype}")


if __name__ == "__main__":
    main()  # 直接运行本脚本时才执行导出。
