from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

# Khởi tạo chuẩn xác thực Bearer Token
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Kiểm tra token gửi từ Frontend (Authorization: Bearer <token>)
    Dùng Firebase Admin SDK để giải mã và xác thực.
    """
    token = credentials.credentials
    try:
        # Nếu token hợp lệ, hàm này trả về một dictionary chứa thông tin user (uid, email...)
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token không hợp lệ hoặc đã hết hạn: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )