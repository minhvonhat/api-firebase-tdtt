from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import db_service
from app.services import ai_service

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

@router.post("/", response_model=ChatResponse)
async def handle_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Endpoint chính để xử lý tin nhắn từ người dùng.
    1. Xác thực người dùng.
    2. Lấy thông tin user từ DB (hoặc tạo mới).
    3. Lấy toàn bộ dữ liệu quán ăn làm ngữ cảnh.
    4. Gọi Gemini để sinh câu trả lời.
    5. Lưu lại lịch sử chat.
    6. Trả về câu trả lời cho frontend.
    """
    user_uid = current_user.get("uid")
    user_email = current_user.get("email")

    # Đảm bảo user tồn tại trong DB của chúng ta
    db_service.get_or_create_user(db, uid=user_uid, email=user_email)

    # Lấy ngữ cảnh từ DB
    restaurants = db_service.get_all_restaurants_with_menu(db)

    # Gọi AI để lấy câu trả lời
    ai_reply = ai_service.get_recommendation(request.message, restaurants)

    # Lưu lịch sử chat
    db_service.save_chat_history(db, user_id=user_uid, message=request.message, response=ai_reply)

    return ChatResponse(reply=ai_reply)

@router.get("/history")
async def get_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Endpoint đọc dữ liệu: Lấy lịch sử trò chuyện của người dùng hiện tại.
    """
    user_uid = current_user.get("uid")
    history = db_service.get_chat_history(db, user_id=user_uid, limit=limit)
    
    return {"data": history}