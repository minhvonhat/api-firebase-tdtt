from sqlalchemy.orm import Session, joinedload
from app.db import models

def get_or_create_user(db: Session, uid: str, email: str) -> models.User:
    """
    Lấy thông tin user từ DB, nếu chưa có thì tạo mới.
    """
    user = db.query(models.User).filter(models.User.id == uid).first()
    if not user:
        user = models.User(id=uid, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✨ Tạo mới user trong DB: {email} (UID: {uid})")
    return user

def get_all_restaurants_with_menu(db: Session) -> list[models.Restaurant]:
    """
    Lấy tất cả các quán ăn và menu của chúng để làm ngữ cảnh cho AI.
    Sử dụng joinedload để tối ưu hóa query, tránh N+1 problem.
    """
    return db.query(models.Restaurant).options(joinedload(models.Restaurant.menu_items)).all()

def save_chat_history(db: Session, user_id: str, message: str, response: str):
    """
    Lưu lại lịch sử cuộc trò chuyện.
    """
    chat_entry = models.ChatHistory(
        user_id=user_id,
        message=message,
        response=response
    )
    db.add(chat_entry)
    db.commit()
    return chat_entry

def get_chat_history(db: Session, user_id: str, limit: int = 50):
    """
    Lấy danh sách lịch sử chat của user.
    """
    # Sắp xếp theo ID giảm dần để lấy các tin nhắn mới nhất
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == user_id).order_by(models.ChatHistory.id.desc()).limit(limit).all()