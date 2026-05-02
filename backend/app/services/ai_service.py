import os
import google.generativeai as genai
from typing import List
from app.db import models

# Cấu hình Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def format_restaurants_for_prompt(restaurants: List[models.Restaurant]) -> str:
    """
    Chuyển đổi danh sách các đối tượng quán ăn thành một chuỗi văn bản
    để làm ngữ cảnh cho mô hình AI.
    """
    context = "Đây là danh sách các quán ăn và thực đơn có sẵn:\n\n"
    for r in restaurants:
        context += f"- Tên quán: {r.name}\n"
        context += f"  - Địa chỉ: {r.address}\n"
        context += f"  - Loại hình: {r.type}\n"
        context += f"  - Đánh giá: {r.rating}/5\n"
        context += "  - Thực đơn:\n"
        for item in r.menu_items:
            context += f"    - {item.name}: {item.price} VND\n"
        context += "\n"
    return context

def get_recommendation(user_prompt: str, restaurants: List[models.Restaurant]) -> str:
    """
    Gửi yêu cầu đến Gemini API để nhận gợi ý.
    """
    if not GEMINI_API_KEY:
        return "Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env."

    restaurant_context = format_restaurants_for_prompt(restaurants)
    
    system_instruction = (
        "Bạn là một trợ lý AI chuyên nghiệp, am hiểu về ẩm thực tên là Minke. "
        "Nhiệm vụ của bạn là gợi ý các quán ăn cho người dùng dựa trên danh sách có sẵn. "
        "Hãy trả lời một cách thân thiện, tự nhiên và chỉ dựa vào thông tin được cung cấp. "
        "Nếu không tìm thấy quán phù hợp, hãy nói rằng bạn không tìm thấy và gợi ý người dùng đưa ra yêu cầu khác. "
        "Đừng bịa đặt thông tin. Trả lời bằng tiếng Việt."
    )
    
    full_prompt = f"{restaurant_context}\n\nDựa vào danh sách trên, hãy trả lời câu hỏi của người dùng: '{user_prompt}'"

    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=system_instruction
        )
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f" Lỗi khi gọi Gemini: {e}")
        return "Xin lỗi, Minke đang gặp sự cố kết nối với bộ não AI. Vui lòng thử lại sau."