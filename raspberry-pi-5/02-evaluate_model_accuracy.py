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
CONF_THRESHOLD = 0.1
NUM_THREADS = 4                    # Raspberry Pi 4 has 4 cores

SHOW_WINDOW = True                # this is a batch evaluation run; set True to also watch it live
DISPLAY_WIDTH = 720                # width of the live preview window only; does not affect inference

FRAME_SKIP = 1                     # process every Nth frame (1 = process all frames)
PRINT_EVERY_N_FRAMES = 1           # print a progress line every N processed frames

CLASS_NAMES = {
    0: "1",
    1: "10",
}

# Ground truth: every frame in this video is known to contain exactly these
# counts of each class. Used to score the model's detections per frame.
GT_COUNTS = {
    "1": 6,     # 1 baht coin
    "10": 4,    # 10 baht coin
}
GT_TOTAL_PER_FRAME = sum(GT_COUNTS.values())

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
        "Otherwise set SHOW_WINDOW = False."
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
    """
    Draws detections on the frame and returns per-class detection counts
    for this frame, e.g. {"1": 5, "10": 4}. Unknown class ids are counted
    under their raw string id so nothing silently disappears.
    """
    detections = outputs[0][0]
    h, w = frame.shape[:2]
    scale_x = w / IMG_SIZE
    scale_y = h / IMG_SIZE

    class_counts = {}
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

        label = CLASS_NAMES.get(int(cls), str(int(cls)))
        class_counts[label] = class_counts.get(label, 0) + 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{label} {conf:.2f}",
            (x1, max(y1 - 5, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    return frame, class_counts


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
print(f"Ground truth per frame: {GT_COUNTS} (total {GT_TOTAL_PER_FRAME} objects/frame)")
print()

frame_idx = 0
processed_count = 0
fps_sum = 0.0

# Evaluation accumulators
class_detected_total = {label: 0 for label in GT_COUNTS}   # raw detections summed over all frames
class_correct_total = {label: 0 for label in GT_COUNTS}    # capped at GT count per frame (true positives)
class_extra_total = {label: 0 for label in GT_COUNTS}       # detections beyond GT count per frame (false positives)
other_class_total = 0                                       # detections of classes not in GT_COUNTS
perfect_frame_count = 0                                     # frames where every class count matched GT exactly
zero_detection_frame_count = 0                               # frames where nothing was detected at all

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

        frame, class_counts = postprocess(outputs, frame)

        frame_total_detected = sum(class_counts.values())
        if frame_total_detected == 0:
            zero_detection_frame_count += 1

        frame_is_perfect = True
        for label, gt_count in GT_COUNTS.items():
            detected = class_counts.get(label, 0)
            class_detected_total[label] += detected
            class_correct_total[label] += min(detected, gt_count)
            if detected > gt_count:
                class_extra_total[label] += detected - gt_count
            if detected != gt_count:
                frame_is_perfect = False

        for label, detected in class_counts.items():
            if label not in GT_COUNTS:
                other_class_total += detected
                frame_is_perfect = False

        if frame_is_perfect:
            perfect_frame_count += 1

        if processed_count % PRINT_EVERY_N_FRAMES == 0:
            counts_str = ", ".join(
                f"{label}: {class_counts.get(label, 0)}/{gt_count}"
                for label, gt_count in GT_COUNTS.items()
            )
            print(
                f"Frame {frame_idx + 1}/{total_frames} - {counts_str} - FPS: {inference_fps:.2f}"
            )

        cv2.putText(
            frame,
            f"FPS: {inference_fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

        if SHOW_WINDOW:
            display_frame = frame
            if DISPLAY_WIDTH and frame_w > DISPLAY_WIDTH:
                display_scale = DISPLAY_WIDTH / frame_w
                display_h = int(frame_h * display_scale)
                display_frame = cv2.resize(frame, (DISPLAY_WIDTH, display_h))

            cv2.imshow("YOLO ONNX Accuracy Evaluation", display_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    frame_idx += 1

cap.release()
if SHOW_WINDOW:
    cv2.destroyAllWindows()

# ==========================
# SUMMARY
# ==========================
avg_fps = fps_sum / processed_count if processed_count else 0.0
gt_total_all_frames = GT_TOTAL_PER_FRAME * processed_count
correct_total_all_frames = sum(class_correct_total.values())
overall_accuracy = (correct_total_all_frames / gt_total_all_frames * 100) if gt_total_all_frames else 0.0
perfect_frame_rate = (perfect_frame_count / processed_count * 100) if processed_count else 0.0

print()
print("=" * 50)
print("EVALUATION SUMMARY")
print("=" * 50)
print(f"Total frames processed          : {processed_count}")
print(f"Expected objects per frame      : {GT_TOTAL_PER_FRAME} ({GT_COUNTS})")
print(f"Frames with zero detections     : {zero_detection_frame_count}")
print(f"Frames with exact correct count : {perfect_frame_count} / {processed_count} ({perfect_frame_rate:.2f}%)")
print()
print("Per-class results:")
for label, gt_count in GT_COUNTS.items():
    expected_total = gt_count * processed_count
    detected_total = class_detected_total[label]
    correct_total = class_correct_total[label]
    extra_total = class_extra_total[label]
    missed_total = expected_total - correct_total
    class_accuracy = (correct_total / expected_total * 100) if expected_total else 0.0
    print(f"  Class \"{label}\":")
    print(f"    Expected total (GT)     : {expected_total}")
    print(f"    Detected total (raw)    : {detected_total}")
    print(f"    Correctly detected      : {correct_total}")
    print(f"    Missed                  : {missed_total}")
    print(f"    Extra / false positives : {extra_total}")
    print(f"    Detection rate          : {class_accuracy:.2f}%")

if other_class_total:
    print(f"  Detections of unexpected classes: {other_class_total}")

print()
print(f"Overall detection accuracy      : {overall_accuracy:.2f}%")
print(f"Average FPS                     : {avg_fps:.2f}")
print("=" * 50)
