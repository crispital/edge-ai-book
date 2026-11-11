"""第二章共用操作：默认CPU，路径相对本目录，沿用官方MNIST网络。"""
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from torchvision import datasets, transforms
from official_mnist.main import Net
ROOT = Path(__file__).resolve().parent
TRANSFORM = transforms.Compose([transforms.ToTensor(), transforms.Normalize((.1307,), (.3081,))])
def load_model(weights):
    model = Net().cpu()
    model.load_state_dict(torch.load(weights, map_location='cpu', weights_only=True))
    return model.eval()  # 关闭Dropout的随机丢弃
def samples(data_root=None, count=10):
    if data_root is None:
        images=[Image.open(ROOT/'样例'/f'mnist_test_{i:04d}.png').convert('L') for i in range(count)]
        return torch.stack([TRANSFORM(im) for im in images])
    ds=datasets.MNIST(data_root,train=False,download=True,transform=TRANSFORM)
    return torch.stack([ds[i][0] for i in range(count)])
def compare(weights, onnx_path, data_root=None):
    import onnxruntime as ort
    x=samples(data_root)
    model=load_model(weights)
    with torch.no_grad(): reference=model(x).numpy()
    session=ort.InferenceSession(str(onnx_path),providers=['CPUExecutionProvider'])
    actual=session.run(None,{session.get_inputs()[0].name:x.numpy()})[0]
    assert actual.shape==reference.shape and np.isfinite(actual).all()
    error=np.abs(actual.astype(np.float64)-reference.astype(np.float64))
    close=bool(np.allclose(actual,reference,rtol=1e-4,atol=1e-5))
    if not close: raise AssertionError('输出未满足组合容差')
    return {'预测':actual.argmax(1).tolist(),'最大绝对误差':float(error.max()),'容差通过':close}
