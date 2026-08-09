import sys
from pathlib import Path
from ultralytics import YOLO

DATA_YAML = Path("/Users/panya/Projects/RMUT/dataset/data.yaml")
MODEL_NAME = "yolo26n.pt"

# ============================================================
#   Training Config
# ============================================================

EPOCHS = 30
IMAGE_SIZE = 640
BATCH_SIZE = 16
DEVICE = "cpu"
RUN_NAME = "rmut_yolo26n"

# ============================================================
print(f"Loading base model: {MODEL_NAME}")
model = YOLO(MODEL_NAME)

print(f"Starting training run '{RUN_NAME}'")
print(f"  data:       {DATA_YAML}")
print(f"  epochs:     {EPOCHS}")
print(f"  image size: {IMAGE_SIZE}")
print(f"  batch size: {BATCH_SIZE}")
print(f"  device:     {DEVICE if DEVICE else 'auto'}")

results = model.train(
    data=str(DATA_YAML),
    epochs=EPOCHS,
    imgsz=IMAGE_SIZE,
    batch=BATCH_SIZE,
    device=DEVICE if DEVICE else None,
    name=RUN_NAME,
  
)

print("\nTraining finished.")
print(f"Results and best weights saved under: runs/detect/{RUN_NAME}/")
print(f"Best weights file: runs/detect/{RUN_NAME}/weights/best.pt")



