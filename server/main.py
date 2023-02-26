from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo

app = FastAPI()

from database import (fetch_one_todo,fetch_all_todos,create_todo,update_todo,delete_todo)

origins = ['https://localhost:3000','http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def read_root():
    return {"Ping":"Pong"}

@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo/{title}",response_model = Todo)
async def get_todo_by_title(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    else:
        raise HTTPException(404,"There isn't Todo item with this title {title}")

@app.post("/api/todo")
async def post_todo(todo:Todo):
    response = await create_todo(todo.dict())
    if response:
        return "Succesfully Insert Todo Item!"
    else:
        raise HTTPException(400,"Something went wrong / Bad Request")

@app.put("/api/todo/{title}",response_model = Todo)
async def put_todo(title:str,desc:str):
    response = await update_todo(title,desc)
    if response:
        return response
    else:
        raise HTTPException(404,"There isn't Todo item with this title {title}")

@app.delete("/api/todo/{title}")
async def remove_todo(title):
    response = await delete_todo(title)
    if response:
        return "Succesfully Delete Todo Item!"
    else:
        raise HTTPException(404,"There isn't Todo item with this title {title}")