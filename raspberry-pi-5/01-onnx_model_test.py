import os
import glob
import time

import cv2
import numpy as np
import onnxruntime as ort

# ==========================
# CONFIG
# ==========================
MODEL_PATH = "best.onnx"          # path to the exported ONNX model
VIDEO_PATH = "VideoTest.mp4"      # path to the test video

IMG_SIZE = 320                     # must match the size used at export/training
CONF_THRESHOLD = 0.2
NUM_THREADS = 4                    # Raspberry Pi 4 has 4 cores

SHOW_WINDOW = True                 # show a live window (requires a display: HDMI, VNC, or X11 forwarding)
DISPLAY_WIDTH = 720                # width of the live preview window only; does not affect inference or saved video

FRAME_SKIP = 1                     # process every Nth frame (1 = process all frames)
CLASS_NAMES = {
    0: "1",
    1: "10",
}

# ==========================
# AUTO-DETECT INPUT FILES
# ==========================
def resolve_path(configured_path, patterns):
    if os.path.isfile(configured_path):
        return configured_path
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            print(f"CONFIG path '{configured_path}' not found, using '{matches[0]}' instead")
            return matches[0]
    raise FileNotFoundError(f"Could not find a file for '{configured_path}'")


MODEL_PATH = resolve_path(MODEL_PATH, ["*.onnx"])
VIDEO_PATH = resolve_path(VIDEO_PATH, ["*.mp4", "*.avi", "*.mov", "*.mkv"])

print(f"Model : {MODEL_PATH}")
print(f"Video : {VIDEO_PATH}")

if SHOW_WINDOW and os.name == "posix" and not os.environ.get("DISPLAY"):
    raise RuntimeError(
        "SHOW_WINDOW is True but no DISPLAY is set. "
        "Run this with a monitor attached to the Pi (desktop session), "
        "or connect over VNC, or SSH with 'ssh -X' for X11 forwarding. "
        "Otherwise set SHOW_WINDOW = False and SAVE_OUTPUT = True instead."
    )

# ==========================
# LOAD MODEL
# ==========================
so = ort.SessionOptions()
so.intra_op_num_threads = NUM_THREADS

session = ort.InferenceSession(
    MODEL_PATH,
    sess_options=so,
    providers=["CPUExecutionProvider"],
)

input_name = session.get_inputs()[0].name
input_shape = session.get_inputs()[0].shape
output_names = [o.name for o in session.get_outputs()]

print(f"Input name  : {input_name}")
print(f"Input shape : {input_shape}")
print(f"Output names: {output_names}")


# ==========================
# PRE / POST PROCESS
# ==========================
def preprocess(frame):
    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return np.ascontiguousarray(img)


def postprocess(outputs, frame):
    detections = outputs[0][0]
    h, w = frame.shape[:2]
    scale_x = w / IMG_SIZE
    scale_y = h / IMG_SIZE

    num_boxes = 0
    for det in detections:
        if len(det) < 6:
            continue
        x1, y1, x2, y2, conf, cls = det[:6]
        if conf < CONF_THRESHOLD:
            continue

        x1 = int(x1 * scale_x)
        y1 = int(y1 * scale_y)
        x2 = int(x2 * scale_x)
        y2 = int(y2 * scale_y)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = CLASS_NAMES.get(int(cls), str(int(cls)))
        cv2.putText(
            frame,
            f"{label} {conf:.2f}",
            (x1, max(y1 - 5, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )
        num_boxes += 1

    return frame, num_boxes


# ==========================
# VIDEO LOOP
# ==========================
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

src_fps = cap.get(cv2.CAP_PROP_FPS) or 25
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Video size  : {frame_w}x{frame_h}")
print(f"Source FPS  : {src_fps:.2f}")
print(f"Total frames: {total_frames}")

frame_idx = 0
processed_count = 0
fps_sum = 0.0
last_annotated = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_idx % FRAME_SKIP == 0:
        input_tensor = preprocess(frame)

        start = time.time()
        outputs = session.run(output_names, {input_name: input_tensor})
        end = time.time()

        inference_fps = 1.0 / (end - start)
        fps_sum += inference_fps
        processed_count += 1

        frame, num_boxes = postprocess(outputs, frame)

        cv2.putText(
            frame,
            f"FPS: {inference_fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

        if processed_count % 30 == 0:
            print(f"Frame {frame_idx}/{total_frames} - FPS: {inference_fps:.2f} - boxes: {num_boxes}")

        last_annotated = frame

    if SHOW_WINDOW:
        display_frame = frame
        if DISPLAY_WIDTH and frame_w > DISPLAY_WIDTH:
            display_scale = DISPLAY_WIDTH / frame_w
            display_h = int(frame_h * display_scale)
            display_frame = cv2.resize(frame, (DISPLAY_WIDTH, display_h))

        cv2.imshow("YOLO ONNX End-to-End", display_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    frame_idx += 1

cap.release()
if SHOW_WINDOW:
    cv2.destroyAllWindows()

avg_fps = fps_sum / processed_count if processed_count else 0.0
print("Done.")
print(f"Processed frames : {processed_count}")
print(f"Average FPS      : {avg_fps:.2f}")
