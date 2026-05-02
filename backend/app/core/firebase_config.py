import os
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """Khởi tạo Firebase Admin SDK"""
    # Kiểm tra xem app đã được khởi tạo chưa để tránh lỗi initialize nhiều lần
    if not firebase_admin._apps:
        # Đường dẫn tới file serviceAccountKey.json nằm ở thư mục gốc của backend
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cred_path = os.path.join(base_dir, 'serviceAccountKey.json')
        
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin SDK khởi tạo thành công.")
        except Exception as e:
            print(f"❌ Lỗi khởi tạo Firebase: {e}")
            print("Vui lòng đảm bảo bạn đã đặt file serviceAccountKey.json tại thư mục backend.")