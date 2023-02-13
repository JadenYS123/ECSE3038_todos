from fastapi import FastAPI, Request, HTTPException
from bson import ObjectId
import motor.motor_asyncio
import pydantic
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

origins = [
    "http://localhost.80000",
    "https://ecse3038-lab3-tester.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://jaden123:Jaden123@ac-3wetz71-shard-00-00.js0j7bp.mongodb.net:27017,ac-3wetz71-shard-00-01.js0j7bp.mongodb.net:27017,ac-3wetz71-shard-00-02.js0j7bp.mongodb.net:27017/?ssl=true&replicaSet=atlas-12i224-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.todo_list

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

password = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    Username: str
    Favourite_Colour: str | None = None
    Role: str | None = None

def fake_decode_token(token):
    return User(
        Username = token + "Jaden", Favourite_Colour = "Red", Role = "John Doe"
    )


