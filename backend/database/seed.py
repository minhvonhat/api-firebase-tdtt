import os
import sys

# Thêm thư mục backend vào sys.path để Python có thể import được package 'app'
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.db.database import SessionLocal, engine
from app.db import models

# Đảm bảo các bảng đã được tạo trước khi chèn dữ liệu
models.Base.metadata.create_all(bind=engine)

def seed_data_from_sql(sql_file_path: str):
    db = SessionLocal()
    try:
        # Kiểm tra nếu DB đã có dữ liệu thì không nạp lại để tránh trùng lặp hoặc báo lỗi
        if db.query(models.Restaurant).count() > 0:
            print("Database đã có dữ liệu. Bỏ qua nạp dữ liệu mẫu (seed).")
            return

        if not os.path.exists(sql_file_path):
            print(f"Không tìm thấy file SQL tại: {sql_file_path}")
            return

        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        print(f"Đang nạp dữ liệu mẫu từ file {os.path.basename(sql_file_path)}...")
        # Sử dụng raw_connection của SQLite để chạy được nhiều câu lệnh (có dấu ;) trong 1 file
        connection = engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.executescript(sql_script)
            connection.commit()
            print(f"Đã chạy thành công file SQL: {sql_file_path}")
        finally:
            connection.close()
                
    except Exception as e:
        print(f"Có lỗi xảy ra khi chạy file SQL: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Đường dẫn trỏ tới file data.sql nằm cùng thư mục 'database'
    sql_file = os.path.join(os.path.dirname(__file__), 'data.sql') 
    seed_data_from_sql(sql_file)