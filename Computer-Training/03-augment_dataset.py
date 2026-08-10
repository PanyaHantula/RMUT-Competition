import sys
from pathlib import Path
import albumentations as A
import cv2

DATASET_DIR = Path(r"D:\RMUT\dataset")
AUGMENTATIONS_PER_IMAGE = 3     # How many augmented copies to generate per original training image
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# ============================================================
def build_augmentation_pipeline():
    return A.Compose(
        [
            A.HorizontalFlip(p=0.5),
            A.Rotate(limit=10, p=0.5, border_mode=cv2.BORDER_CONSTANT),
            A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.6),
            A.HueSaturationValue(hue_shift_limit=15, sat_shift_limit=30, val_shift_limit=20, p=0.5),
            A.Affine(translate_percent=0.1, scale=(0.8, 1.2), p=0.5),
            A.Blur(blur_limit=3, p=0.2),
        ],
        bbox_params=A.BboxParams(format="yolo", label_fields=["class_labels"], min_visibility=0.3),
    )


def read_yolo_label(label_path: Path):
    if not label_path.exists():
        return []
    lines = label_path.read_text(encoding="utf-8").strip().splitlines()
    boxes = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        class_id, x_c, y_c, w, h = parts
        boxes.append((int(class_id), float(x_c), float(y_c), float(w), float(h)))
    return boxes


def write_yolo_label(label_path: Path, boxes):
    lines = [f"{cid} {x:.6f} {y:.6f} {w:.6f} {h:.6f}" for cid, x, y, w, h in boxes]
    label_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    train_images_dir = DATASET_DIR / "images" / "train"
    train_labels_dir = DATASET_DIR / "labels" / "train"

    if not train_images_dir.exists():
        sys.exit(f"ERROR: Train images folder not found at: {train_images_dir}")
    if not train_labels_dir.exists():
        sys.exit(f"ERROR: Train labels folder not found at: {train_labels_dir}")

    original_images = sorted(
        p for p in train_images_dir.iterdir()
        if p.suffix.lower() in IMAGE_EXTS and "_aug" not in p.stem
    )

    if not original_images:
        sys.exit(f"No original training images found in: {train_images_dir}")

    pipeline = build_augmentation_pipeline()

    print(f"Found {len(original_images)} original training images.")
    print(f"Generating {AUGMENTATIONS_PER_IMAGE} augmented copies per image...")

    total_created = 0
    total_skipped = 0

    for image_path in original_images:
        label_path = (train_labels_dir / image_path.stem).with_suffix(".txt")
        boxes = read_yolo_label(label_path)
        if not boxes:
            total_skipped += 1
            continue

        image = cv2.imread(str(image_path))
        if image is None:
            total_skipped += 1
            continue
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        class_labels = [b[0] for b in boxes]
        bboxes = [(b[1], b[2], b[3], b[4]) for b in boxes]

        for i in range(AUGMENTATIONS_PER_IMAGE):
            new_stem = f"{image_path.stem}_aug{i + 1}"
            new_image_path = train_images_dir / f"{new_stem}{image_path.suffix}"
            new_label_path = train_labels_dir / f"{new_stem}.txt"

            if new_image_path.exists() and new_label_path.exists():
                continue  # already generated in a previous run

            try:
                augmented = pipeline(image=image_rgb, bboxes=bboxes, class_labels=class_labels)
            except Exception as e:
                print(f"  WARNING: augmentation failed for {image_path.name} (copy {i + 1}): {e}")
                continue

            if not augmented["bboxes"]:
                # all bounding boxes fell outside the frame after transform -- skip this copy
                continue

            aug_image_bgr = cv2.cvtColor(augmented["image"], cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(new_image_path), aug_image_bgr)

            new_boxes = [
                (cls, *bbox) for cls, bbox in zip(augmented["class_labels"], augmented["bboxes"])
            ]
            write_yolo_label(new_label_path, new_boxes)
            total_created += 1

    if total_skipped:
        print(f"WARNING: Skipped {total_skipped} images (missing/empty label or unreadable image)")

    final_count = len(list(train_images_dir.glob("*")))
    print(f"\nDone. New augmented files created: {total_created}")
    print(f"Train set now has {final_count} images total (original + augmented).")

if __name__ == "__main__":
    main()
