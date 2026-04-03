# Nexus

## รายละเอียดโปรเจค

NexusFix เป็นเว็บไซต์ที่พัฒนาด้วย Django Framework
มีวัตถุประสงค์เพื่อ ระบบจัดการข้อมูล / ระบบแสดงสินค้า 

---

## ฟีเจอร์ของระบบ (Features)

*  ระบบสมัครสมาชิก / เข้าสู่ระบบ
*  จัดการข้อมูล (เพิ่ม / แก้ไข / ลบ)
*  แสดงข้อมูลบนหน้าเว็บ
*  รองรับการแสดงรูปภาพ 

---

## เทคโนโลยีที่ใช้

* Python
* Django Framework
* SQLite
* HTML / CSS / Bootstrap

---

## วิธีติดตั้ง 

```bash
# Clone โปรเจค
git clone https://github.com/droply2550/NexusFix.git
(https://github.com/droply2550/NexusFix.git)

# เข้าโฟลเดอร์โปรเจค
cd NexusFix/Nexus

# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน (Windows)
venv\Scripts\activate

pip install Pillow
pip freeze > requirements.txt
pip install -r requirements.txt

```

---

## วิธีรันโปรเจค

```bash
python manage.py check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

เข้าใช้งานได้ที่: http://127.0.0.1:8000/
```
---

## ตัวอย่างหน้าเว็บ

(ใส่รูปแคปหน้าจอ เช่น)

![home](NexusShop/Nexus/cardshop/static/images/home.png)
![product](NexusShop/Nexus/cardshop/static/images/product.png)
![contact](NexusShop/Nexus/cardshop/static/images/contact.png)
![about](NexusShop/Nexus/cardshop/static/images/about.png)
![cart](NexusShop/Nexus/cardshop/static/images/cart.png)

---

## 📂 โครงสร้างโปรเจค (Project Structure)

```
NEXUSFIX-MAIN/
│
├── Nexus/                          # โฟลเดอร์รวบรวมแอปและไฟล์สื่อ
│   ├── cardshop/                   # [App] แอปพลิเคชันหลักของระบบร้านการ์ด
│   │   ├── __pycache__/            # ไฟล์ Compiled Python
│   │   ├── migrations/             # เก็บประวัติการเปลี่ยนแปลง Database
│   │   ├── static/                 # เก็บไฟล์ CSS, JS, Images ของแอปนี้
│   │   ├── templates/              # เก็บไฟล์หน้าเว็บ HTML ของแอปนี้
│   │   ├── __init__.py             
│   │   ├── admin.py                # ตั้งค่าหน้า Admin สำหรับจัดการข้อมูลการ์ด
│   │   ├── apps.py                 # ตั้งค่าชื่อแอป
│   │   ├── forms.py                # จัดการฟอร์ม (เช่น ฟอร์มเพิ่มสินค้า/สมัครสมาชิก)
│   │   ├── models.py               # ออกแบบตาราง Database (เช่น สินค้าการ์ด, คำสั่งซื้อ)
│   │   ├── tests.py                # สำหรับเขียนโค้ดทดสอบระบบ
│   │   ├── urls.py                 # เส้นทาง URL ภายในแอป (เช่น /shop/, /detail/)
│   │   └── views.py                # ตัวประมวลผล Logic และแสดงหน้าเว็บ
│   │
│   └── media/                      # เก็บไฟล์ที่อัปโหลดจริง
│       └── cards/                  # (ย่อย) เก็บรูปภาพสินค้าประเภทการ์ด
│
├── nexus_project/                  # โฟลเดอร์ตั้งค่าหลักของโปรเจกต์
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py                     # สำหรับการเชื่อมต่อแบบ Asynchronous (เช่น Chat)
│   ├── settings.py                 # ใช้ตั้งค่า Database, แอป, และ Path
│   ├── urls.py                     # รวม URL จากทุกแอปเข้าด้วยกัน
│   └── wsgi.py                     # สำหรับการ Deploy ขึ้น Server ทั่วไป
│
├── db.sqlite3                      # ฐานข้อมูลเริ่มต้น (ใช้ในขั้นตอนพัฒนา)
└── manage.py                       # สั่งการ Django (runserver, migrate, createsuperuser)

```

---

## ผู้พัฒนา

* ชื่อ: นาย ภูมิอนันต์ จะวะนะ
* รหัสนักศึกษา: 68090902

* ชื่อ: นาย สุรภัทร จันทร์นาคา
* รหัสนักศึกษา: 68068075

* ชื่อ: นาย พรพิพัฒน์ วงษสุวรรณ์
* รหัสนักศึกษา: 68074788

---

## หมายเหตุ

โปรเจคนี้เป็นส่วนหนึ่งของรายวิชา ICT12367
