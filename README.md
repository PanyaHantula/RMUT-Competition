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
- [3. ติดตั้ง Python](#3-ติดตั้ง-python)
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

*** หมายเหตุ เครื่องคอมพิวเตอร์สำหรับการฝึกฝน ให้ติดตั้ง python 3.11 เท่านั้น ****

---

## 2. ติดตั้ง VS Code
ดาวน์โหลดและติดตั้ง VS Code จากเว็บไซต์ทางการ:
[https://code.visualstudio.com/](https://code.visualstudio.com/)

---

## 3. ติดตั้ง Python 3.11

ดาวน์โหลดและติดตั้ง Python3.11 จากเว็บไซต์ทางการ:
[https://www.python.org/downloads/release/python-3110/]
(https://www.python.org/downloads/release/python-3110/)

ตรวจสอบว่าติดตั้งสำเร็จด้วยคำสั่ง:
*** Command Prompt --> Run as administrator ***

```cmd
winget install Python.Python.3.11
python --version
```

ปิด Command Prompt 

---

## 4. สร้าง Virtual Environment
สร้าง virtual environment โดยใช้ Python :

เปิด Command Prompt 

```cmd
d:
mkdir RMUT
cd RMUT
python -m venv rmut-env
```

เปิดใช้งาน (activate) environment:
**Windows (CMD)**
```cmd
.\rmut-env\Scripts\activate.bat
```
---

## 5. ติดตั้งแพ็กเกจ Python
หลังจากเปิดใช้งาน virtual environment แล้ว ให้ติดตั้งแพ็กเกจที่จำเป็นดังนี้:
## 5.1 Update pip 
```cmd
python.exe -m pip install --upgrade pip
```
## 5.2 Download requirement.txt 
Download requirement.txt จาก.....
นำไปไว้ใน Folder --> D:\RMUT

## 5.3 Install requirements
```cmd
pip install -r requirements.txt
```

## 6. Extract Dataset
run script

```cmd
python 01-video_extraction.py
```
---

## 7. ตั้งค่า Label Studio
เปิด Command Prompt (หน้าต่างใหม่)
ก่อนเปิดใช้งาน Label Studio ต้องตั้งค่าตัวแปรสภาพแวดล้อม (environment variables) เพื่อให้สามารถโหลดชุดข้อมูลขนาดใหญ่จากเครื่องได้อย่างถูกต้อง

```cmd
d:
mkdir RMUT
cd RMUT
.\rmut-env\Scripts\activate.bat
```

start Label-Studio
```cmd
set NLTK_DISABLE_IMPORT_SECURITY=1
set LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
set LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=D:\RMUT\data
label-studio start
```

> **หมายเหตุ:** ตัวแปรสภาพแวดล้อมเหล่านี้จะมีผลเฉพาะใน terminal session ปัจจุบันเท่านั้น ต้องตั้งค่าใหม่ทุกครั้งที่เปิด terminal ใหม่ หรือเพิ่มเข้าไปใน shell profile (`.zshrc`, `.bashrc`) หรือ startup script เพื่อให้ค่าคงอยู่ถาวร

## 8. เพิ่มรูปภาพเข้าใน label-Studio 
- เพิ่มรูปภาพเข้าใน label-Studio 
- Label Image
- Export JSON

---

## 9. Export Dataset
run script

```cmd
python 02-export_dataset.py
```
## 10. Augmentation Dataset
run script

```cmd
python 03-augment_dataset.py
```

## 11. Train Model
run script

```cmd
python 04-train_yolo26n.py
```

## 12. Validation Model
run script

```cmd
python 05-yolo-video-validation.py
```

## 13. Convert .pt Model to .onnx model
run script

```cmd
python 06-onnx_convert.py
```

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

- **โหมดการนำเข้าข้อมูลใน Label Studio:** ให้ใช้ **Local Files Storage** แทนการอัปโหลดไฟล์โดยตรง สำหรับชุดข้อมูลขนาดใหญ่ 
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

> **หมายเหตุ:** ควรตรวจสอบให้ค่า `IMG_SIZE` ในตรงกับค่า `imgsz` ที่ใช้ตอน export โมเดลเป็น ONNX เสมอ 
