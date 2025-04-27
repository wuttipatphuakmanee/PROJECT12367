<h1 align="center">🎤 คาราโอเกะซิตี้ - ระบบจองห้องคาราโอเกะด้วย Django</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2%2B-green?logo=django" alt="Django Version">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap" alt="Bootstrap Version">
  </p>

<p align="center">
  <em>ระบบสำหรับจองห้องคาราโอเกะผ่านเว็บไซต์ พัฒนาด้วย Django Framework</em>
</p>

<p align="center">
  <img src="https://img2.pic.in.th/pic/unlog_index.png" alt="Karaoke Screenshot" style="max-width: 90%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</p>

---

## 🧠 เทคโนโลยีที่ใช้ (Tech Stack)

* **Backend:** Django
* **Frontend:** Bootstrap 5
* **Database (Development):** SQLite
* **Authentication:** Django's built-in Auth (แยก User/Admin)

---

## 🚀 ฟีเจอร์หลัก (Features)

* 👤 **ระบบสมาชิก:**
    * ลงทะเบียน (Register)
    * เข้าสู่ระบบ (Login)
    * (ตัวเลือก) ลืมรหัสผ่านผ่านอีเมล
* 🔒 **การยืนยันตัวตน:**
    * บังคับให้ผู้ใช้ล็อกอินก่อนทำการจองห้อง
* 📅 **ระบบการจอง:**
    * แสดงรายการห้องว่างให้เลือก
    * ฟอร์มสำหรับกรอกข้อมูลการจอง (ชื่อ, วันเวลาเริ่มต้น-สิ้นสุด)
    * แสดงหน้ายืนยันเมื่อการจองสำเร็จ
    * แสดงรายการจองทั้งหมดของผู้ใช้ (หรือทั้งหมดในระบบ)
    * แก้ไขและลบการจองได้
* 💰 **การคำนวณ:**
    * คำนวณระยะเวลาการจอง (ชั่วโมง)
    * คำนวณค่าบริการตามราคาห้องและระยะเวลา
* 📞 **การติดต่อ:**
    * หน้าฟอร์มสำหรับติดต่อ/แจ้งปัญหา (ผ่าน Modal ใน Base Template)

---

## 🖼 ตัวอย่างหน้าจอระบบ (Screenshots)

<details>
<summary><strong>🗟 หน้าแรก (ยังไม่ล็อกอิน)</strong></summary>
<img src="https://img2.pic.in.th/pic/unlog_index.png" width="100%" />
</details>

<details>
<summary><strong>🔐 หน้าล็อกอิน</strong></summary>
<img src="https://img5.pic.in.th/file/secure-sv1/loginea5e91541540bc07.png" width="100%" />
</details>

<details>
<summary><strong>📝 สมัครสมาชิก</strong></summary>
<img src="https://img5.pic.in.th/file/secure-sv1/register6791888483ebc4eb.png" width="100%" />
</details>

<details>
<summary><strong>🎶 หน้าเลือกจองห้อง (หลังล็อกอิน)</strong></summary>
<img src="https://img5.pic.in.th/file/secure-sv1/log_index.png" width="100%" />
</details>

<details>
<summary><strong>📝 ฟอร์มจองห้องคาราโอเกะ</strong></summary>
<img src="https://img5.pic.in.th/file/secure-sv1/booking_form.png" width="100%" />
</details>

<details>
<summary><strong>💯 หน้าเมื่อจองห้องเสร็จ</strong></summary>
<img src="https://img5.pic.in.th/file/secure-sv1/booking_success.png" width="100%" />
</details>

<details>
<summary><strong>📜 ประวัติการจองทั้งหมด</strong></summary>
<img src="https://img5.pic.in.th/file/secure-sv1/booking_all.png" width="100%" />
</details>

<details>
<summary><strong>📞 ติดต่อ/แจ้งปัญหา</strong></summary>
<img src="https://img2.pic.in.th/pic/contact4571975733950869.png" width="100%" />
</details>

---

## 🧱 โครงสร้างโปรเจกต์ (Project Structure)
karaoke_project/
├── karaoke_project/      # Project configuration (settings.py, urls.py)
├── accounts/             # Django App: User authentication (login, register)
├── booking/              # Django App: Core booking functionality
│   ├── migrations/       # Database migration files
│   ├── templates/        # HTML templates for the booking app
│   │   └── booking/
│   │       ├── base.html

│   │       ├── room_list.html

│   │       ├── booking_form.html

│   │       ├── booking_success.html

│   │       └── all_bookings.html

│   ├── admin.py

│   ├── apps.py

│   ├── forms.py

│   ├── models.py

│   ├── tests.py          # Test file (currently empty)
│   ├── urls.py

│   └── views.py

├── manage.py             # Django's command-line utility
└── README.md             # This file
*(โครงสร้างอาจแสดงเฉพาะส่วนที่สำคัญ)*

---

## 🚀 วิธีรันโปรเจกต์ (Development Mode)

1.  **Clone Repository (ถ้ามี):**
    ```bash
    # git clone <your-repository-url>
    # cd karaoke_project
    ```
    *(นำ comment ออก ถ้าคุณ clone มาจาก Git)*

2.  **สร้างและ Activate Virtual Environment (แนะนำ):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **ติดตั้ง Dependencies:**
    ```bash
    pip install django
    # เพิ่ม library อื่นๆ ที่จำเป็น ถ้ามี
    # pip install -r requirements.txt (ถ้ามีไฟล์ requirements.txt)
    ```

4.  **Run Database Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **สร้าง Superuser (สำหรับเข้าหน้า Admin):**
    ```bash
    python manage.py createsuperuser
    ```
    (ทำตามขั้นตอนที่ปรากฏบนหน้าจอ)

6.  **รัน Development Server:**
    ```bash
    python manage.py runserver
    ```
    โปรเจกต์จะพร้อมใช้งานที่ `http://127.0.0.1:8000/`

---

## 💌 ติดต่อผู้พัฒนา (Contributors)

<div align="center">

| ช่องทาง     | minkpn                                                    | Wuttipat                                                          | Patlom                                                  |
| :---------- | :-------------------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------ |
| **📧 Email** | <a href="mailto:minkridsada233@gmail.com">Gmail</a>        | <a href="mailto:wuttipatphuakmaneeo@gmail.com">Gmail</a>             | <a href="mailto:Teeraphat15.km@gmail.com">Gmail</a>      |
| **🔗 GitHub** | <a href="https://github.com/minkpn">minkpn</a>             | <a href="https://github.com/wuttipatphuakmanee">Wuttipat</a>         | <a href="https://github.com/Teerapatkm">Patlom</a>         |
| **💬 Line** | `@minkpn`                                                 | `@Wuttipat`                                                       | `@Patlom`                                               |

</div>

---

<h3 align="center">✨ Made with ❤️ by minkpn x Wuttipat x Patlom ✨</h3>
