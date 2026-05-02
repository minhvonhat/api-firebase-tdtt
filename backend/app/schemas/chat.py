from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Schemas cho dữ liệu trả về từ API ---

class MenuItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    price: float

class RestaurantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    rating: Optional[float] = None
    menu_items: List[MenuItemResponse] = []

# --- Schemas cho tương tác Chat ---

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str