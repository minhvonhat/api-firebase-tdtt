from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True) # Sử dụng Firebase UID làm khóa chính
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Mối quan hệ: Một User có thể có nhiều tin nhắn
    chats = relationship("ChatHistory", back_populates="user")

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    rating = Column(Float, default=0.0)
    price_range = Column(Integer, default=0)
    open_time = Column(String(50))
    close_time = Column(String(50))
    type = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Mối quan hệ: Một quán ăn có nhiều món trong menu (Xóa quán ăn thì xóa luôn menu)
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete")

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    food_type = Column(String(100))
    ingredients = Column(Text)
    story = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    restaurant = relationship("Restaurant", back_populates="menu_items")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    message = Column(Text, nullable=False)    # Tin nhắn từ người dùng
    response = Column(Text, nullable=False)   # Câu trả lời từ AI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="chats")