from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Базовый маршрут
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/greet/{name}")
async def greet(name: str = "Alice"):
    return {"message": f"Hello, {name}!"}

@app.get("/search")
async def search(query: str = "python"):
    return {"message": f"You searched for: {query}"}

# Различные типы данных
@app.get("/json")
async def get_json():
    return {
        "name": "Alex Smith",
        "age": 25,
        "hobbies": ["coding", "hiking", "photography"]
    }

@app.get("/file")
async def get_file():
    # Создаем временный файл
    with open("sample.txt", "w") as f:
        f.write("asdasdcxasxcasd")
    return FileResponse("sample.txt")

@app.get("/redirect")
async def redirect():
    return RedirectResponse(url="/")

# Работа с заголовками и куками
@app.get("/headers")
async def get_headers(request: Request):
    return dict(request.headers)

@app.get("/set-cookie")
async def set_cookie():
    response = JSONResponse(content={"message": "Cookie has been set successfully"})
    response.set_cookie(key="username", value="alex123")
    return response

@app.get("/get-cookie")
async def get_cookie(request: Request):
    username = request.cookies.get("username", "guest")
    return {"username": username}

# Обработка данных запроса
@app.post("/login")
async def login(username: str = Form(default="john"), password: str = Form(default="secret123")):
    return {"message": f"Welcome, {username}!"}

class RegisterData(BaseModel):
    username: str = "newuser"
    email: str = "newuser@example.com"
    password: str = "mypassword123"

@app.post("/register")
async def register(data: RegisterData):
    return {"message": f"User {data.username} registered successfully!"}

# Работа с классами
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

users = [
    User(id=1, username="mary", email="mary@example.com", password="pass123"),
    User(id=2, username="peter", email="peter@example.com", password="secure456")
]

@app.get("/users", response_model=List[User])
async def get_users():
    return users

@app.get("/users/{id}", response_model=User)
async def get_user(id: int = 1):
    for user in users:
        if user.id == id:
            return user
    return {"error": "User not found"}

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)