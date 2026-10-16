"""用固定MNIST测试样本检查PyTorch与ONNX导出的数值一致性。"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort
import torch
from torchvision import datasets, transforms


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))  # 只导入模型，不执行训练。
from main import Net


def compare(reference, actual, atol=1e-5, rtol=1e-4):
    """先检查形状和有限值，再以PyTorch输出为参考计算误差。"""
    if reference.shape != actual.shape or reference.size == 0:
        raise ValueError("输出形状必须相同且不能为空")
    if not (np.isfinite(reference).all() and np.isfinite(actual).all()):
        raise ValueError("输出含NaN或无穷大，不能进行有效数值比较")
    error = np.abs(actual.astype(np.float64) - reference.astype(np.float64))
    nonzero = reference != 0  # 参考值为零时，不定义相对误差。
    relative = error[nonzero] / np.abs(reference[nonzero])
    return {
        "passed": bool(np.all(error <= atol + rtol * np.abs(reference))),
        "max_abs_error": float(error.max()),
        "max_rel_error_nonzero": float(relative.max()) if relative.size else None,
        "zero_reference_count": int((~nonzero).sum()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=PROJECT_ROOT / "data")
    parser.add_argument("--weights", type=Path,
                        default=PROJECT_ROOT / "model" / "mnist_cnn.pt")
    parser.add_argument("--onnx", type=Path,
                        default=PROJECT_ROOT / "outputs" / "mnist_cnn.onnx")
    parser.add_argument("--output-dir", type=Path,
                        default=PROJECT_ROOT / "outputs" / "regression")
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("输出目录已存在，请用--output-dir指定新目录")

    model = Net().cpu()
    state = torch.load(args.weights, map_location="cpu", weights_only=True)
    model.load_state_dict(state, strict=True)
    model.eval()  # 关闭本模型中Dropout的随机行为。
    session = ort.InferenceSession(
        str(args.onnx), providers=["CPUExecutionProvider"],
    )
    input_meta, = session.get_inputs()  # 本例只有一个输入、一个输出。
    output_meta, = session.get_outputs()
    if (input_meta.name, input_meta.type, input_meta.shape) != (
        "input", "tensor(float)", [1, 1, 28, 28],
    ):
        raise ValueError("ONNX输入接口与本例约定不一致")
    if (output_meta.name, output_meta.type, output_meta.shape) != (
        "log_probs", "tensor(float)", [1, 10],
    ):
        raise ValueError("ONNX输出接口与本例约定不一致")

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])
    dataset = datasets.MNIST(
        args.data_dir, train=False, download=False, transform=transform,
    )
    inputs, labels, references, actuals, rows = [], [], [], [], []
    atol, rtol = 1e-5, 1e-4  # 运行前固定，本次教学实验不据结果调整。
    with torch.inference_mode():
        for index in range(10):
            image, label = dataset[index]
            tensor = image.unsqueeze(0)  # 固定batch=1，不能一次输入10张。
            array = tensor.numpy()       # 两侧使用完全相同的float32输入。
            reference = model(tensor).numpy()
            actual, = session.run([output_meta.name], {input_meta.name: array})
            metrics = compare(reference, actual, atol, rtol)
            rows.append({
                "index": index, "label": label,
                "pytorch_class": int(reference.argmax(axis=1)[0]),
                "onnx_class": int(actual.argmax(axis=1)[0]), **metrics,
            })
            inputs.append(array)
            labels.append(label)
            references.append(reference)
            actuals.append(actual)

    summary = compare(np.concatenate(references), np.concatenate(actuals))
    summary.update({"atol": atol, "rtol": rtol, "samples": rows})
    args.output_dir.mkdir(parents=True, exist_ok=False)  # 不覆盖已有实验。
    np.savez_compressed(
        args.output_dir / "outputs.npz", inputs=np.concatenate(inputs),
        labels=labels, indices=np.arange(10),
        pytorch=np.concatenate(references), onnx=np.concatenate(actuals),
    )
    result = json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False)
    (args.output_dir / "summary.json").write_text(result + "\n", encoding="utf-8")
    print(result)
    print(f"保存位置：{args.output_dir.resolve()}")
    if not summary["passed"]:
        raise SystemExit(1)  # 超出容差仍先保存结果，便于排查。


if __name__ == "__main__":
    main()
