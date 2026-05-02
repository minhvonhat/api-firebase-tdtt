import os
import requests
from dotenv import load_dotenv

# Xác định thư mục gốc của dự án để đọc file .env
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, '.env')

if os.path.exists(ENV_PATH):
    load_dotenv(dotenv_path=ENV_PATH)

# Lấy URL của backend từ biến môi trường, nếu không có thì mặc định là localhost
BACKEND_API_URL = os.getenv("BACKEND_URL", "http://localhost:8000").strip()

def signup(email, password):
    url = f"{BACKEND_API_URL}/api/auth/signup"
    response = requests.post(url, json={"email": email, "password": password})    
    if not response.ok:
        try:
            # Cố gắng lấy chi tiết lỗi từ JSON response của backend
            error_detail = response.json().get("detail", response.text)
        except requests.exceptions.JSONDecodeError:
            error_detail = response.text
        # Ném lỗi với thông điệp chi tiết hơn
        raise requests.HTTPError(error_detail)
    return response.json()

def login(email, password):
    url = f"{BACKEND_API_URL}/api/auth/login"
    response = requests.post(url, json={"email": email, "password": password})
    if not response.ok:
        try:
            error_detail = response.json().get("detail", response.text)
        except requests.exceptions.JSONDecodeError:
            error_detail = response.text
        raise requests.HTTPError(error_detail)
    return response.json()

def send_chat(id_token: str, message: str):
    """
    Gửi tin nhắn đến backend và nhận phản hồi từ AI.
    """
    url = f"{BACKEND_API_URL}/api/chat/"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.post(url, json={"message": message}, headers=headers)
    if not response.ok:
        try:
            error_detail = response.json().get("detail", response.text)
        except requests.exceptions.JSONDecodeError:
            error_detail = response.text
        raise requests.HTTPError(error_detail)
    return response.json()

def get_chat_history(id_token: str, limit: int = 50):
    """
    Lấy danh sách lịch sử trò chuyện của người dùng.
    """
    url = f"{BACKEND_API_URL}/api/chat/history"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.get(url, headers=headers, params={"limit": limit})
    if not response.ok:
        try:
            error_detail = response.json().get("detail", response.text)
        except requests.exceptions.JSONDecodeError:
            error_detail = response.text
        raise requests.HTTPError(error_detail)
    return response.json()