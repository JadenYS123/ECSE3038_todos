from fastapi import FastAPI, Request, HTTPException
from bson import ObjectId
import motor.motor_asyncio
import pydantic

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://week4:Lb30oh1KEZTEVypf@cluster0.cklfqkn.mongodb.net/?retryWrites=true&w=majority")
db = client.todo_list

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str


@app.post("/todos")
async def create_new_todo(request: Request):
    todo_object = await request.json()

    new_todo = await db["todos"].insert_one(todo_object)
    created_todo = await db["todos"].find_one({"_id": new_todo.inserted_id})

    return created_todo


@app.get("/todos")
async def get_all_todos():
    todos = await db["todos"].find().to_list(999)
    return todos

@app.get("/todo/{id}")
async def get_one_todo_by_id(id: str):
    todo = await db["todos"].find_one({"_id": ObjectId(id)})
    return todo
