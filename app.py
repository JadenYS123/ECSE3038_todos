from fastapi import FastAPI, Request, HTTPException
from bson import ObjectId
import motor.motor_asyncio
import pydantic
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
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
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://jaden123:Jaden123@ac-3wetz71-shard-00-00.js0j7bp.mongodb.net:27017,ac-3wetz71-shard-00-01.js0j7bp.mongodb.net:27017,ac-3wetz71-shard-00-02.js0j7bp.mongodb.net:27017/?ssl=true&replicaSet=atlas-12i224-shard-0&authSource=admin&retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
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


@app.get("/profile")
async def get_profile():
    profile = await db["profile"].find().to_list(999)
    if len(profile) < 1:
        return {}
    return profile[0]


@app.post("/profile",status_code=201)
async def create_new_profile(request:Request):
    
    profile_obj = await request.json()
    profile_obj["last_updated"]=datetime.now()

    new_profile = await db["profile"].insert_one(profile_obj)
    latest_profile = await db["profile"].find_one({"_id": new_profile.inserted_id})

    return latest_profile
@app.post("/data",status_code=201)
async def create_new_profile(request:Request):
    tank_obj = await request.json()

    new_tank = await db["tank"].insert_one(tank_obj)
    created_tank = await db["tank"].find_one({"_id": new_tank.inserted_id})

    return created_tank

@app.get("/data")
async def retrieve_tanks():
    tanks = await db["tank"].find().to_list(999)
    return tanks

@app.delete("/data/{id}",status_code=204)
async def delete_tank(id: str):

    found= await db["tank"].find_one({"_id": ObjectId(id)})
    if (found) is None:
        raise HTTPException(status_code=404, detail="Item not found")

    remove_tank= await db["tank"].delete_one({"_id":ObjectId(id)})

    return {"message":"ITEM WAS DELETED "}

    
    

@app.patch("/data/{id}")
async def do_update(id:str, request: Request):
    updated= await request.json()
    result = await db["tank"].update_one({"_id":ObjectId(id)}, {'$set': updated})
    
    if result.modified_count == 1:
         if (
                updated_tank := await db["tank"].find_one({"_id": id})
            ) is not None:
                return updated_tank   
    else:
         raise HTTPException(status_code=404, detail="Item not found")
