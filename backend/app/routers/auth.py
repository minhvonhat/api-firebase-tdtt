import os
import requests
from fastapi import APIRouter, HTTPException
from app.schemas.auth import AuthRequest

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup")
async def signup(request: AuthRequest):
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Thiếu cấu hình FIREBASE_API_KEY trong .env")
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {"email": request.email, "password": request.password, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"]["message"])
        
    return {"message": "Đăng ký thành công", "localId": data["localId"]}

@router.post("/login")
async def login(request: AuthRequest):
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Thiếu cấu hình FIREBASE_API_KEY trong .env")
        
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": request.email, "password": request.password, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"]["message"])
        
    return {"message": "Đăng nhập thành công", "id_token": data["idToken"], "localId": data["localId"]}