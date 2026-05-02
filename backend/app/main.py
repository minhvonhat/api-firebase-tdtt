import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

# 1. Load các biến môi trường từ file .env trước khi làm bất cứ việc gì khác
load_dotenv()

# Thêm thư mục backend vào sys.path để có thể import trực tiếp từ database.seed
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.core.firebase_config import initialize_firebase
from app.routers import auth, chat

from app.db.database import engine, SessionLocal
from app.db import models
from database.seed import seed_data_from_sql

# Tạo các bảng trong CSDL SQLite nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)

# --- AUTO SEED DATA ---
def auto_seed_data():
    try:
        sql_file_path = os.path.join(backend_dir, "database", "data.sql")
        seed_data_from_sql(sql_file_path)
    except Exception as e:
        print(f"Lỗi khi tự động nạp dữ liệu: {e}")

auto_seed_data()

# 2. Khởi tạo Firebase Admin SDK
initialize_firebase()

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Restaurant Recommendation Bot API",
    description="API cho chatbot gợi ý quán ăn sử dụng Firebase và Gemini API",
    version="1.0.0"
)

# Cấu hình CORS để Frontend (Streamlit) có thể giao tiếp với Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường thực tế nên thay "*" bằng domain cụ thể của frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Đăng ký các Router xử lý API
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Chào mừng đến với API Chatbot gợi ý quán ăn!"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running healthy"}

# In danh sách API ra terminal khi khởi động
print("\n" + "="*50)
print(" DANH SÁCH CÁC API ENDPOINTS ĐÃ ĐĂNG KÝ:")
for route in app.routes:
    if hasattr(route, "methods") and hasattr(route, "path"):
        # Loại bỏ phương thức OPTIONS (mặc định của CORS) cho dễ nhìn
        methods = ", ".join(route.methods - {"OPTIONS"})
        if methods:
            print(f"  - {methods: <7} : {route.path}")
print("="*50 + "\n")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)