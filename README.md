# Tuition Fees for Computer & AI Engineering from TCAS68

## คำอธิบายเกี่ยวกับโปรเจกต์นี้
โปรเจกต์นี้จัดทำขึ้นเพื่อสำรวจข้อมูลขอค่าใช้จ่ายในการศึกษาสำหรับหลักสูตรที่เกี่ยวข้องทางด้านวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์ เพื่อที่จะทำให้เป็นประโยชน์ในการตัดสินใจสำหรับผู้ที่ต้องการเข้าศึกษาต่อในระดับมหาวิทยาลัยที่มีความเกี่ยงข้องทางด้านคอมพิวเตอร์และปัญญาประดิษฐ์

## ขั้นตอนในการทำ Dashboard และจุดเด่นของ Dashboard

### 1. การดึงข้อมูล
- มีการดึงข้อมูลหลักสูตรจากไฟล์ JSON ของ MyTCAS โดยใช้ไฟล์ `extractor.py` ในการดึงข้อมูล
- มีการกรองข้อมูลเฉพาะที่อยู่ใน keywords ได้แก่ วิศวกรรมคอมพิวเตอร์, วิศวกรรมปัญญาประดิษฐ์, Computer Engineering และ Artificial Intelligence Engineering
- ดึงมาเฉพาะประเภทข้อมูลที่สนใจ ได้แก่ ชื่อมหาวิทยาลัย วิทยาเขตของมหาลัย คณะ หลักสูตร และค่าใช้จ่ายในการศึกษา
- บันทึกข้อมูลที่ได้ลงในไฟล์ excel

### 2. การจัดการข้อมูล
- ใช้ไฟล์ `cleaned_data.ipynb` ในการจัดการข้อมูล
- ตรวจสอบว่าในข้อมูลใน dataset ที่ดึงมาได้อยู่ในขอบเขตของลักสูตรที่เกี่ยวข้องทางด้านวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์
- จัดการจัดหมวดหมู่ของค่าใช้จ่ายการศึกษา(Tuition Category) ว่าเป็นประเภทไหน จากคอลัมน์ค่าใช้จ่ายในการศึกษา(Tuition Fee)
- ใช้ keyword เช่น ค่าเรียนตลอดหลักสูตร ค่าเทอม เป็นต้น ในการเก็บข้อมูลค่าเทอมตามความเป็นจริงจากจากคอลัมน์ค่าใช้จ่ายในการศึกษา(Tuition Fee)
- ข้อมูลค่าใช้จ่ายในการศึกษา(Tuition Fee) ที่ไม่ได้บอกอย่างชัดเจน ทำการค้นหาข้อมูลจากมหาวิทยาลัยที่ทำการสอนหลักสูตรแล้วเก็บเอาไว้ใน dataset
- บันทึกข้อมูลที่ทำการ cleaning เรียบร้อย เพื่อนำไปใช้ในการสร้าง dashboard ต่อ

### 3. Dashboard
-  ใช้ plotly dash ในการสร้าง Dashboard ขึ้นมาจากไฟล์ `app.py`
-  Feature ที่โดดเด่น:
    - Bar Chart แสดงค่าใช้จ่ายในการศึกษาที่สามารถเลือกดูได้ทั้งแบบค่าเทอมและค่าเรียนตลอดหลักสูตรกับเลือกมหาวิทยาลัยเพื่อเปรียบเทียบ (สามารถเลือกได้หลายแห่ง)
    - Pie Chart แสดงจำนวนหลักสูตรที่เปิดสอนทางด้านวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์ในแต่ละมหาวิทยาลัย
    - ตารางข้อมูลหลักสูตรด้านวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์
    - ข้อมูลสถิติค่าใช้จ่ายสำหรับหลักสูตรด้านวิศวกรรมคอมพิวเตอร์และวิศวกรรมปัญญาประดิษฐ์

# Tuition Fees for Computer & AI Engineering from TCAS68(2025)

## Project Description

This project was created to explore tuition cost data for programs related to **Computer Engineering** and **Artificial Intelligence Engineering**. The goal is to provide helpful insights for prospective students considering university studies in computer and AI-related fields in Thailand.

## Steps for Creating the Dashboard and Key Features

### 1. Data Extraction
- Program data is extracted from a JSON file provided by MyTCAS using the `extractor.py` script.
- The data is filtered to include only relevant keywords: `วิศวกรรมคอมพิวเตอร์`, `วิศวกรรมปัญญาประดิษฐ์`, `Computer Engineering`, and `Artificial Intelligence Engineering`.
- Only specific fields are collected: **University**, **Campus**, **Faculty**, **Program**, and **Tuition Fee**.
- The extracted data is saved into an Excel file.

### 2. Data Cleaning
- Data processing is performed in the `cleaned_data.ipynb` notebook.
- The dataset is reviewed to ensure it contains only programs related to Computer Engineering and AI Engineering.
- The **Tuition Category** is classified based on the raw text in the **Tuition Fee** column.
- Keywords such as `total course fee`, `semester tuition`, etc., are used to extract actual tuition values.
- When the tuition fee is not clearly stated, manual research is conducted using university websites to fill in the missing data.
- Cleaned data is saved and used for building the dashboard.

### 3. Dashboard
- The dashboard is developed using **Plotly Dash** in the `app.py` file.

#### Key Features:
- 📊 **Bar Chart**:
  - Compare tuition fees by selecting universities.
  - Toggle between total program fee and per-semester fee.
- 🥧 **Pie Chart**:
  - Visualizes the number of Computer Engineering and AI programs offered by each university.
- 📋 **Program Table**:
  - Lists all Computer Engineering and Artificial Intelligence Engineering programs with details.
- 📈 **Statistical Summary**:
  - Displays overall statistics for tuition costs across the selected programs.



  

