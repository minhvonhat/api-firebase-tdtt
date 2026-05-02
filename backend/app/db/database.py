import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Xác định thư mục backend/ và thư mục gốc của dự án
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

# Đọc file .env để script lấy được cấu hình khi chạy độc lập
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# Lấy cấu hình DB từ biến môi trường
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/chatbot.db")

# Nếu là đường dẫn SQLite tương đối, chuyển thành đường dẫn tuyệt đối
if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///./"):
    db_name = SQLALCHEMY_DATABASE_URL.split("/")[-1]
    db_path = os.path.join(BACKEND_DIR, db_name).replace("\\", "/")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

# Nếu là SQLite thì cần thêm thuộc tính check_same_thread
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# Khởi tạo engine kết nối
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

# SessionLocal dùng để tương tác với DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()