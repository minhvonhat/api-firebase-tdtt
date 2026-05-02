# api-firebase-tdtt
Bài thực hành số 2 - APPLICATION PROGRAMMING INTERFACE AND FIREBASE STUDIO

## 1. Video Demo
**[ Nhấn vào đây để xem Video Demo của nhóm](#)** *(Lưu ý: Bạn hãy thay dấu `#` bằng link YouTube/Google Drive của bạn)*

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

## 5. Cấu trúc thư mục dự án
project_root/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── firebase_config.py      # Cấu hình Firebase (chỉ dùng để xác thực đăng nhập)
│   │   ├── db/                         # Thư mục mới: Quản lý cơ sở dữ liệu SQL
│   │   │   ├── database.py             # Cấu hình và khởi tạo kết nối SQL (SQLAlchemy bằng Python)
│   │   │   └── models.py               # Định nghĩa các bảng SQL (VD: Users, ChatHistory, Restaurants)
│   │   ├── dependencies/
│   │   │   └── auth.py                 # Các dependency kiểm tra token người dùng từ Firebase
│   │   ├── routers/
│   │   │   ├── auth.py                 # Các endpoint API cho đăng nhập/đăng xuất
│   │   │   └── chat.py                 # Các endpoint API xử lý chat và gợi ý quán
│   │   ├── schemas/
│   │   │   ├── auth.py                 # Pydantic models kiểm tra dữ liệu đầu vào/ra của Auth
│   │   │   └── chat.py                 # Pydantic models kiểm tra dữ liệu đầu vào/ra của Chat
│   │   ├── services/
│   │   │   ├── db_service.py           # Chứa các hàm xử lý logic thao tác với SQL (thêm, sửa, xóa, lấy dữ liệu)
│   │   │   └── ai_service.py          # Logic kết nối với GEMINI bằng Python
│   │   └── main.py                     # File gốc khởi tạo ứng dụng FastAPI
│   │
│   ├── database/                       # Thư mục chứa script và dữ liệu mẫu
│   │   ├── data.sql                    # Dữ liệu quán ăn (SQL)
│   │   └── seed.py                     # Script nạp dữ liệu vào CSDL (Được gọi tự động khi khởi chạy main.py)
│   └── chatbot.db                      # File cơ sở dữ liệu vật lý (nếu bạn dùng SQLite, nằm ngang cấp với thư mục app)
│
├── frontend/                           # Thư mục giao diện tách biệt hoàn toàn
│   ├── api_client.py                   # Các hàm Python tiện ích gửi request HTTP tới backend
│   └── app.py                          # Mã nguồn giao diện chính (chạy bằng Streamlit)
│
├── .gitignore                          # Bỏ qua các file không đưa lên GitHub (vd: chatbot.db, thư mục __pycache__, serviceAccountKey.json)
├── requirements.txt                    # Khai báo các thư viện Python cho toàn dự án
└── README.md                           # Tài liệu hướng dẫn cài đặt và chạy dự án
