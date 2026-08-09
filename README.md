# RMUT-Competition

# การแข่งขันราชมงคลวิชาการวิศวกรรมระดับชาติ ครั้งที่ 17
## หัวข้อ "แข่งขันพัฒนาโมเดลปัญญาประดิษฐ์สำหรับอุปกรณ์ Raspberry Pi 5"

# คู่มือการติดตั้งระบบ (Installation Guide)

คู่มือนี้อธิบายขั้นตอนการติดตั้งสภาพแวดล้อมและการรัน pipeline ทั้งหมดของโปรเจกต์ ตั้งแต่การตั้งค่าสภาพแวดล้อม → การเก็บข้อมูล → การติด label → การเพิ่มข้อมูล (augmentation) → การเทรนโมเดล → การตรวจสอบผลลัพธ์ → การแปลงโมเดล

## สารบัญ

- [1. สิ่งที่ต้องเตรียมก่อนติดตั้ง](#1-สิ่งที่ต้องเตรียมก่อนติดตั้ง)
- [2. ติดตั้ง VS Code](#2-ติดตั้ง-vs-code)
- [3. ติดตั้ง Python 3.11](#3-ติดตั้ง-python-311)
- [4. สร้าง Virtual Environment](#4-สร้าง-virtual-environment)
- [5. ติดตั้งแพ็กเกจ Python](#5-ติดตั้งแพ็กเกจ-python)
- [6. ตั้งค่า Label Studio](#6-ตั้งค่า-label-studio)
- [7. ขั้นตอนการทำงานของ Pipeline](#7-ขั้นตอนการทำงานของ-pipeline)
- [หมายเหตุ](#หมายเหตุ)

---

## 1. สิ่งที่ต้องเตรียมก่อนติดตั้ง

- เครื่องคอมพิวเตอร์ macOS หรือ Windows
- สามารถเข้าถึง Terminal / Command Prompt ได้
- พื้นที่ว่างในดิสก์ประมาณ 5 GB (สำหรับ dependencies และชุดข้อมูล)

---

## 2. ติดตั้ง VS Code

ดาวน์โหลดและติดตั้ง VS Code จากเว็บไซต์ทางการ:
[https://code.visualstudio.com/](https://code.visualstudio.com/)

---

## 3. ติดตั้ง Python 3.11

ดาวน์โหลดและติดตั้ง Python 3.11 จากเว็บไซต์ทางการ:
[https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)

ตรวจสอบว่าติดตั้งสำเร็จด้วยคำสั่ง:

```bash
python3.11 --version
```

---

## 4. สร้าง Virtual Environment

สร้าง virtual environment โดยใช้ Python 3.11:

```bash
python3.11 -m venv rmut-env
```

เปิดใช้งาน (activate) environment:

**macOS / Linux**
```bash
source rmut-env/bin/activate
```

**Windows (CMD)**
```cmd
rmut-env\Scripts\activate.bat
```

**Windows (PowerShell)**
```powershell
rmut-env\Scripts\Activate.ps1
```

---

## 5. ติดตั้งแพ็กเกจ Python

หลังจากเปิดใช้งาน virtual environment แล้ว ให้ติดตั้งแพ็กเกจที่จำเป็นดังนี้:

```bash
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install ultralytics
pip install onnxruntime
pip install pillow
pip install opencv-python
pip install numpy
pip install matplotlib
pip install label-studio
```

---

## 6. ตั้งค่า Label Studio

ก่อนเปิดใช้งาน Label Studio ต้องตั้งค่าตัวแปรสภาพแวดล้อม (environment variables) เพื่อให้สามารถโหลดชุดข้อมูลขนาดใหญ่จากเครื่องได้อย่างถูกต้อง

### macOS / Linux

```bash
export NLTK_DISABLE_IMPORT_SECURITY=1
export DATA_UPLOAD_MAX_MEMORY_SIZE=1073741824
export DATA_UPLOAD_MAX_NUMBER_FILES=100000
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/Users/panya/Projects/RMUT/data
```

### Windows (Command Prompt)

```cmd
set NLTK_DISABLE_IMPORT_SECURITY=1
set DATA_UPLOAD_MAX_MEMORY_SIZE=1073741824
set DATA_UPLOAD_MAX_NUMBER_FILES=100000
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
set LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=C:\Users\panya\Projects\RMUT\data
```

### Windows (PowerShell)

```powershell
$env:NLTK_DISABLE_IMPORT_SECURITY = "1"
$env:DATA_UPLOAD_MAX_MEMORY_SIZE = "1073741824"
$env:DATA_UPLOAD_MAX_NUMBER_FILES = "100000"
$env:LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED = "true"
$env:LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT = "C:\Users\panya\Projects\RMUT\data"
```

> **หมายเหตุ:** ตัวแปรสภาพแวดล้อมเหล่านี้จะมีผลเฉพาะใน terminal session ปัจจุบันเท่านั้น ต้องตั้งค่าใหม่ทุกครั้งที่เปิด terminal ใหม่ หรือเพิ่มเข้าไปใน shell profile (`.zshrc`, `.bashrc`) หรือ startup script เพื่อให้ค่าคงอยู่ถาวร

---

## 7. ขั้นตอนการทำงานของ Pipeline

รันสคริปต์ตามลำดับต่อไปนี้ โดยต้องเปิดใช้งาน virtual environment ไว้ก่อน

| ขั้นตอน | สคริปต์ | คำอธิบาย |
|------|--------|-------------|
| 6  | `00-videorecord.py` | บันทึกวิดีโอต้นฉบับสำหรับชุดข้อมูล |
| 7  | `01-video_extraction.py` | ดึงเฟรม/ภาพจากวิดีโอที่บันทึกไว้ |
| 8  | `label-studio` | เปิดใช้งาน Label Studio และติด label ภาพ**ทั้งหมด**ในชุดข้อมูล |
| 9  | `03-augment_dataset.py` | เพิ่มข้อมูล (augmentation) ให้กับชุดข้อมูลที่ติด label แล้ว |
| 10 | `04-train_yolo26n.py` | เทรนโมเดล YOLO |
| 11 | `05-yolo-video-validation.py` | ตรวจสอบผลลัพธ์ของโมเดลกับวิดีโอ |
| 12 | — | แปลงไฟล์โมเดลจาก `model.pt` เป็น `model.onnx` |

### คำสั่งตามลำดับขั้นตอน

```bash
# 6. บันทึกวิดีโอ
python 00-videorecord.py

# 7. ดึงเฟรมจากวิดีโอ
python 01-video_extraction.py

# 8. เปิด Label Studio และติด label ภาพทั้งหมด
label-studio

# 9. เพิ่มข้อมูล (augment) ให้ชุดข้อมูลที่ติด label แล้ว
python 03-augment_dataset.py

# 10. เทรนโมเดล YOLO
python 04-train_yolo26n.py

# 11. ตรวจสอบผลลัพธ์ของโมเดลกับวิดีโอ
python 05-yolo-video-validation.py

# 12. แปลงโมเดลเป็น ONNX (ตัวอย่างการใช้ Ultralytics CLI)
yolo export model=model.pt format=onnx
```

---

## หมายเหตุ

- **โหมดการนำเข้าข้อมูลใน Label Studio:** ให้ใช้ **Local Files Storage** แทนการอัปโหลดไฟล์โดยตรง สำหรับชุดข้อมูลขนาดใหญ่ และตั้งค่าโหมดการนำเข้าเป็น **"Files"** ไม่ใช่ **"Tasks (JSON/JSONL/Parquet)"**
- **รูปแบบการ Export:** ฟังก์ชัน export ในตัวของ Label Studio อย่าง "YOLO with Images" / "COCO with Images" จะ**ไม่คัดลอกรูปภาพ**เมื่อใช้ Local Storage ให้ export เป็นไฟล์ JSON ธรรมดา แล้วใช้สคริปต์แปลงข้อมูลเองแทน
- **ระบบพิกัด Bounding Box:** Label Studio จะ export bounding box เป็นเปอร์เซ็นต์ โดยอ้างอิงจากมุมซ้ายบน (0–100) ในขณะที่ YOLO ต้องการรูปแบบที่ normalize แล้วและอ้างอิงจากจุดกึ่งกลาง (0–1) ต้องแปลงค่าให้ถูกต้องตามรูปแบบนี้
- ปิดการใช้งาน virtual environment เมื่อใช้งานเสร็จแล้ว:
  ```bash
  deactivate
  ```
