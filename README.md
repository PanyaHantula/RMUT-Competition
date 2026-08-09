# การแข่งขันราชมงคลวิชาการวิศวกรรมระดับชาติ ครั้งที่ 17

## หัวข้อ "แข่งขันพัฒนาโมเดลปัญญาประดิษฐ์สำหรับอุปกรณ์ Raspberry Pi 5"

# คู่มือการติดตั้งระบบ (Installation Guide)

คู่มือนี้แบ่งออกเป็น 2 ส่วนหลัก:

- **ส่วนที่ 1** — การติดตั้งเครื่องคอมพิวเตอร์สำหรับการ Training Model
- **ส่วนที่ 2** — การติดตั้งบน Raspberry Pi 5 (สำหรับรันโมเดลที่เทรนเสร็จแล้ว)

## สารบัญ

**ส่วนที่ 1: การติดตั้งเครื่องคอมพิวเตอร์สำหรับการ Training Model**
- [1. สิ่งที่ต้องเตรียมก่อนติดตั้ง](#1-สิ่งที่ต้องเตรียมก่อนติดตั้ง)
- [2. ติดตั้ง VS Code](#2-ติดตั้ง-vs-code)
- [3. ติดตั้ง Python 3.11](#3-ติดตั้ง-python-311)
- [4. สร้าง Virtual Environment](#4-สร้าง-virtual-environment)
- [5. ติดตั้ง Python Packet-site](#5-ติดตั้ง-python-packet-site)
- [6. ตั้งค่า Label Studio](#6-ตั้งค่า-label-studio)
- [7. ตัวอย่าง Code Program สำหรับการเก็บข้อมูลและการ Training YOLO Model](#7-ตัวอย่าง-code-program-สำหรับการเก็บข้อมูลและการ-training-yolo-model)

**ส่วนที่ 2: การติดตั้งบน Raspberry Pi 5**
- [1. เข้าสู่ระบบ Raspberry Pi ผ่าน SSH](#1-เข้าสู่ระบบ-raspberry-pi-ผ่าน-ssh)
- [2. อัปเดตระบบ และเปิดการตั้งค่า VNC](#2-อัปเดตระบบ-และเปิดการตั้งค่า-vnc)
- [3. ติดตั้ง Python และไลบรารีที่จำเป็น](#3-ติดตั้ง-python-และไลบรารีที่จำเป็น)
- [4. สร้าง Python Virtual Environment](#4-สร้าง-python-virtual-environment)
- [5. ติดตั้ง Python Packet-Site](#5-ติดตั้ง-python-packet-site-1)
- [6. ส่งไฟล์ .onnx จากเครื่องคอมพิวเตอร์ไปยัง Raspberry Pi](#6-ส่งไฟล์-onnx-จากเครื่องคอมพิวเตอร์ไปยัง-raspberry-pi)
- [7. ทดสอบโมเดลบน Raspberry Pi](#7-ทดสอบโมเดลบน-raspberry-pi)

---

# ส่วนที่ 1: การติดตั้งเครื่องคอมพิวเตอร์สำหรับการ Training Model

## 1. สิ่งที่ต้องเตรียมก่อนติดตั้ง

- เครื่องคอมพิวเตอร์ macOS หรือ Windows
- สามารถเข้าถึง Terminal / Command Prompt ได้
- พื้นที่ว่างในดิสก์ประมาณ 5 GB (สำหรับ dependencies และชุดข้อมูล)

> **สำคัญ:** เครื่องคอมพิวเตอร์สำหรับการ Training Model ให้ติดตั้ง **Python 3.11** เพื่อให้ Label Studio ใช้งานได้

---

## 2. ติดตั้ง VS Code

1. ดาวน์โหลดและติดตั้ง VS Code จากเว็บไซต์ทางการ: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. ติดตั้ง **Python Extension** ให้เรียบร้อย

---

## 3. ติดตั้ง Python 3.11

ดาวน์โหลดและติดตั้งได้จากช่องทางใดช่องทางหนึ่ง:

- เว็บไซต์ทางการ: [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)
- หรือติดตั้งผ่าน **Microsoft Store** (สำหรับ Windows)

ตรวจสอบว่าติดตั้งสำเร็จ โดยเปิด Command Prompt / Terminal แล้วพิมพ์คำสั่ง:

```bash
python --version
```

---

## 4. สร้าง Virtual Environment

เปิด Command Prompt / Terminal แล้วสร้าง virtual environment โดยใช้ Python 3.11:

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

## 5. ติดตั้ง Python Packet-site

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

ก่อนเปิดใช้งาน Label Studio ต้องตั้งค่าตัวแปรสภาพแวดล้อม (environment variables) เพื่อให้สามารถโหลดชุดข้อมูลขนาดใหญ่จากเครื่องได้อย่างถูกต้อง เปิด Command Prompt / Terminal แล้วพิมพ์คำสั่ง:

**macOS / Linux**
```bash
export NLTK_DISABLE_IMPORT_SECURITY=1
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/Users/panya/Projects/RMUT/data
label-studio start
```

**Windows (Command Prompt)**
```cmd
set NLTK_DISABLE_IMPORT_SECURITY=1
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
set LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=C:\Users\panya\Projects\RMUT\data
label-studio start
```

**Windows (PowerShell)**
```powershell
$env:NLTK_DISABLE_IMPORT_SECURITY = "1"
$env:LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED = "true"
$env:LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT = "C:\Users\panya\Projects\RMUT\data"
label-studio start
```

> **หมายเหตุ:**
> - ตัวแปรสภาพแวดล้อมเหล่านี้จะมีผลเฉพาะใน terminal session ปัจจุบันเท่านั้น ต้องตั้งค่าใหม่ทุกครั้งที่เปิด terminal ใหม่ หรือเพิ่มเข้าไปใน shell profile (`.zshrc`, `.bashrc`) หรือ startup script เพื่อให้ค่าคงอยู่ถาวร
> - โหมดการนำเข้าข้อมูลใน Label Studio: ให้ใช้ **Local Files Storage** แทนการอัปโหลดไฟล์โดยตรง สำหรับชุดข้อมูลขนาดใหญ่

---

## 7. ตัวอย่าง Code Program สำหรับการเก็บข้อมูลและการ Training YOLO Model

| Demo Code | คำอธิบาย |
|---|---|
| `00-videorecord.py` | บันทึกวิดีโอ |
| `01-video_extraction.py` | ดึงเฟรม/ภาพจากวิดีโอที่บันทึกไว้ |
| `02-export_dataset.py` | Export Dataset จาก Label Studio |
| `03-augment_dataset.py` | เพิ่มข้อมูล (augmentation) ให้กับชุดข้อมูลที่ติด label แล้ว |
| `04-train_yolo26n.py` | Train YOLO Model |
| `05-yolo-video-validation.py` | ทดสอบ YOLO Model กับวิดีโอ |
| `06-onnx_convert.py` | แปลงไฟล์โมเดลจาก `model.pt` เป็น `model.onnx` |

```bash
# 00. บันทึกวิดีโอ
python 00-videorecord.py

# 01. ดึงเฟรมจากวิดีโอ
python 01-video_extraction.py

# 02. Export Dataset จาก Label Studio
python 02-export_dataset.py

# 03. เพิ่มข้อมูล (augment) ให้ชุดข้อมูลที่ติด label แล้ว
python 03-augment_dataset.py

# 04. เทรนโมเดล YOLO
python 04-train_yolo26n.py

# 05. ทดสอบโมเดลกับวิดีโอ
python 05-yolo-video-validation.py

# 06. แปลงโมเดลเป็น ONNX
python 06-onnx_convert.py
```

---

# ส่วนที่ 2: การติดตั้งบน Raspberry Pi 5

ขั้นตอนนี้เป็นการเตรียม Raspberry Pi 5 ให้พร้อมสำหรับรันโมเดล ONNX ที่เทรนและแปลงไฟล์เสร็จแล้วจากเครื่องคอมพิวเตอร์หลัก

## 1. เข้าสู่ระบบ Raspberry Pi ผ่าน SSH

```bash
ssh <username>@<raspberry-pi-ip>
```

---

## 2. อัปเดตระบบ และเปิดการตั้งค่า VNC

**อัปเดตระบบ**
```bash
sudo apt update && sudo apt upgrade -y
```

**เปิดใช้งาน VNC**
```bash
sudo raspi-config
```
เลือก **3 Interface Option** → **I3 VNC** → **Yes**

---

## 3. ติดตั้ง Python และไลบรารีที่จำเป็น

```bash
sudo apt install python3-venv
sudo apt install python3-pip
sudo apt install python3-dev
sudo apt install libopenblas-dev
sudo apt install libopenblas0
sudo apt install cmake
sudo apt install build-essential
sudo apt update
```

> **หมายเหตุ:** บน Raspberry Pi OS Bookworm แพ็กเกจ `libatlas-base-dev` ถูกยกเลิกไปแล้ว ให้ใช้ `libopenblas-dev` และ `libopenblas0` แทน

---

## 4. สร้าง Python Virtual Environment

```bash
mkdir rmut
cd rmut
python3 -m venv onnx-env
source onnx-env/bin/activate
```

---

## 5. ติดตั้ง Python Packet-Site

หลังจากเปิดใช้งาน virtual environment แล้ว ให้ติดตั้ง Packet-Site ที่จำเป็นดังนี้:

```bash
pip install --upgrade pip
pip install torch torchvision torchaudio
pip install ultralytics
pip install onnxruntime
pip install pillow
pip install opencv-python
pip install numpy
pip install matplotlib
```

---

## 6. ส่งไฟล์ .onnx จากเครื่องคอมพิวเตอร์ไปยัง Raspberry Pi

```bash
scp best.onnx <username>@<raspberry-pi-ip>:/home/<username>/rmut
```

ตัวอย่าง:

```bash
scp best.onnx rmuti-admin@172.17.11.254:/home/rmuti-admin/rmut
```

---

## 7. ทดสอบโมเดลบน Raspberry Pi

รันสคริปต์เพื่อทดสอบโมเดลบนอุปกรณ์จริง:

```bash
python3 01-onnx_model_test.py
```

รันสคริปต์เพื่อทดสอบโมเดลบนอุปกรณ์จริง และประเมินผล:

```bash
python3 02-evaluate_model_accuracy.py
```

> **หมายเหตุ:** ควรตรวจสอบให้ค่า `IMG_SIZE` ในสคริปต์ inference ตรงกับค่า `imgsz` ที่ใช้ตอน export โมเดลเป็น ONNX เสมอ (ต้องเป็นตัวเลขที่หารด้วย 32 ลงตัว เช่น 320, 480) มิฉะนั้นจะเกิดข้อผิดพลาดที่ Concat layer
