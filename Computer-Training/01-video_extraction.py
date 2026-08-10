import cv2
import os

video_path = "VideoTrain.mp4"
output_folder = "data/images"

target_frames = 30      # Total frame

if not os.path.exists(video_path):
    print(f"Error: Video file not found -> {video_path}")
    exit()
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

print(f"Video FPS: {fps:.2f}")
print(f"Total frames: {total_frames}")
print(f"Duration: {duration:.2f} seconds")

if target_frames >= total_frames:
    frame_interval = 1
    print(f"Warning: target_frames >= total_frames, extracting every frame ({total_frames} frames).")
else:
    frame_interval = total_frames // target_frames

print(f"Calculated frame_interval: {frame_interval} (will extract ~{total_frames // frame_interval} frames)")

frame_count = 0
saved_count = 0

print("Extracting frames...")
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % frame_interval == 0 and saved_count < target_frames:
        filename = f"frame_{saved_count:05d}.jpg"
        filepath = os.path.join(output_folder, filename)
        cv2.imwrite(filepath, frame)
        saved_count += 1

    frame_count += 1

print(f"\nDone !! Extracted {saved_count} frames.")
cap.release()
