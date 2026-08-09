import cv2
import time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()


fps = 30.0
cap.set(cv2.CAP_PROP_FPS, fps)

actual_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Camera set to: {actual_fps} FPS")

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
record_duration = 5 * 60  
frame_interval = 1.0 / fps

is_recording = False
start_time = None
prev_write_time = None

print("Press 'R' to start recording, 'q' to quit.")
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    display_frame = frame.copy()

    if is_recording:
        current_time = time.time()
        elapsed = current_time - prev_write_time

        if elapsed >= frame_interval:
            out.write(frame)
            prev_write_time = current_time

        total_elapsed = time.time() - start_time
        remaining = max(0, record_duration - total_elapsed)
        cv2.putText(display_frame, f"REC {int(total_elapsed)}s / {int(record_duration)}s",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if total_elapsed >= record_duration:
            print("Reached 5 minutes. Stopping recording.")
            break
    else:
        cv2.putText(display_frame, "Press 'R' to start recording",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow('Live Recording', display_frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r') and not is_recording:
        out = cv2.VideoWriter('VideoTest.mp4', fourcc, fps, frame_size)
        is_recording = True
        start_time = time.time()
        prev_write_time = start_time
        print("Recording started...")


    if key == ord('q'):
        print("Stop...")
        break

cap.release()
cv2.destroyAllWindows()

if is_recording:
    print(f"Recording saved successfully. Duration: {total_elapsed:.1f} seconds")
else:
    print("No recording was made.")