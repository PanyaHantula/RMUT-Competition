import cv2
from ultralytics import YOLO

model = YOLO("best.pt")
VIDEO_PATH = "VideoValidation.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
frame_size = 640

if not cap.isOpened():
    print(f"Fail to open video file: {VIDEO_PATH}")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or fail to read frame")
        break

    results = model(frame, imgsz=frame_size, verbose=False)
    annotated_frame = results[0].plot()
    display_frame = cv2.resize(
        annotated_frame,
        (frame_size, int(annotated_frame.shape[0] * frame_size / annotated_frame.shape[1])),
    )

    cv2.imshow("YOLO26n Video Detection", display_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q") or key == 27:
        break

cap.release()
cv2.destroyAllWindows()