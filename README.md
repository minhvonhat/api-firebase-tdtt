# api-firebase-tdtt
Bài thực hành số 2 - APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

## 1. Video Demo
**[ Nhấn vào đây để xem Video Demo](https://drive.google.com/file/d/1WscuroW_I4bLo1AM4v0qiaTQ99c-Qeuz/view?usp=sharing)** 

---

## 2. Hướng dẫn cài đặt môi trường

**Bước 1:** Kéo dự án về máy và di chuyển vào thư mục dự án:
```bash
git clone <link-repo-github-cua-ban>
cd api-firebase-tdtt
```

**Bước 2:** Tạo và kích hoạt môi trường ảo (Virtual Environment):
```bash
# Đối với Windows:
python -m venv .venv
.venv\Scripts\activate
```
**Bước 3:** Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

**Bước 4:** Tạo file `.env` tại thư mục gốc của dự án (ngang cấp với `backend`) và điền các API Key theo yêu cầu (Firebase, Gemini,...).

**Bước 5:** Tải file khóa bảo mật `serviceAccountKey.json` (Firebase Admin SDK) từ Firebase Console và đặt vào **thư mục gốc của dự án** (cùng vị trí với file `.env`).

## 3. Hướng dẫn chạy Backend
Mở terminal (đã kích hoạt môi trường ảo), di chuyển vào thư mục `backend` và khởi động server FastAPI:
```bash
cd backend
uvicorn app.main:app --reload
```

## 4. Hướng dẫn chạy Frontend
Mở thêm một terminal **mới** (nhớ kích hoạt lại môi trường ảo), di chuyển vào thư mục `frontend` và khởi động ứng dụng Streamlit:
```bash
cd frontend
streamlit run app.py
```

---
