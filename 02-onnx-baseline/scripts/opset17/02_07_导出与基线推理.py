"""由hzl权重导出动态批量ONNX，再在同一CPU输入上比较输出。"""
import argparse,json
from pathlib import Path
import torch,onnx
from 模型工具 import ROOT,load_model,samples,compare

def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    model=load_model(ROOT/'模型/hzl.pt'); x=samples()
    target=output/'mnist_cnn.onnx'
    torch.onnx.export(model,x[:1],str(target),opset_version=17,
        input_names=['input'],output_names=['output'],
        dynamic_axes={'input':{0:'batch'},'output':{0:'batch'}})
    onnx.checker.check_model(onnx.load(str(target)))
    return compare(ROOT/'模型/hzl.pt',target)
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT/'运行结果/导出推理'))
    args=parser.parse_args();print(json.dumps(run(args.output),ensure_ascii=False))
