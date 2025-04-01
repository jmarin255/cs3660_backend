from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

@app.get("/")

def read_root():
    return {"message": "hello world"}


class loginRequest(BaseModel):
    username: str
    password: str


def verify_login(username: str, password: str) -> bool:
    try:
        with open("./db/users.json") as file:
            data=json.load(file)
            for user in data ["users"]:
                if user["username"]== username and user ["password"]==password:
                    return True
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="User file not found")

    return False



@app.post("/api/login")
def login(request: loginRequest): 
    if (verify_login(request.username, request.password)):
        return {'success': 'true'}
    raise HTTPException(status_code=401, detail="invalid credentials")