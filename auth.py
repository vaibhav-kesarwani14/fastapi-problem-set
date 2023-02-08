from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/login")

def login():
    return FileResponse('login.html')
    
@app.get("/register")

def register(username, password):
    return {"Usernname": username, "Password": password}