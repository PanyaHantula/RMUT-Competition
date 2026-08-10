from ultralytics import YOLO

CONFIG = {
    "model_path": "best.pt",
    "output_format": "onnx",
    "imgsz": 320,        
    "opset": 12,
    "simplify": True,
    "dynamic": False,
    "half": False,
}

model = YOLO(CONFIG["model_path"])
model.export(
    format=CONFIG["output_format"],
    imgsz=CONFIG["imgsz"],
    opset=CONFIG["opset"],
    simplify=CONFIG["simplify"],
    dynamic=CONFIG["dynamic"],
    half=CONFIG["half"],
)

