from fastapi import FastAPI, Request, Response, HTTPException, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from hashlib import sha256
from jinja2 import Template
from fastapi.responses import RedirectResponse
from peewee import*
import uuid
import peewee
import bcrypt


app = FastAPI()

db = peewee.SqliteDatabase("authentication_data.db")

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField()
    password = CharField()


class Authentication(BaseModel):
    user = ForeignKeyField(User, backref="authentications")
    token = CharField()

class Post(BaseModel):
    user_info = ForeignKeyField(User, to_field='username')
    post_name = CharField()
    caption = CharField()

class Like_Table(peewee.Model):
    user_info_like = ForeignKeyField(User, to_field='username')
    post_id = ForeignKeyField(Post, to_field='id')
    likedBy = CharField()
    like_count = IntegerField()

def create_tables():
    with db:
        db.create_tables([User, Authentication])

if __name__ == '__main__':
    create_tables()



@app.post("/login")
async def login(username, password):
    
    try:
        user = User.get(User.username == username)

        bytes = password.encode('utf-8')
        
        # generating the salt
        salt = bcrypt.gensalt()
        
        # Hashing the password
        hash = bcrypt.hashpw(bytes, salt)

        if User.password == hash:
            token = str(uuid.uuid4())
            Authentication.create(user=user, token=token)
            return {"message": "Login successful", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="Username not found")
    
    response = RedirectResponse(url=f"/posts/{user.username}")
    response.status_code = 302
    return response

@app.post("/sign-up")
async def register(username, email, password):

    bytes = password.encode('utf-8')
        
    # generating the salt
    salt = bcrypt.gensalt()
    
    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    try:
        new_user = User.create(username = username, email = email, password = hash)
    except peewee.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    token = str(uuid.uuid4())
    Authentication.create(user=new_user, token=token)
    return {"message": "User registered", "token": token}

@app.post("/create_post")
async def create_post(request: Request):
    request_data = await request.json()
    token = request.headers.get("Authorization")
    post_name = request_data.get("post_name")
    caption = request_data.get("caption")

    try:
        authentication = Authentication.get(Authentication.token == token)
        user = authentication.user
    except Authentication.DoesNotExist:
        raise HTTPException(status_code=400, detail="Invalid Token")

    try:
        new_post = Post.create(
            user_info=user,
            post_name=post_name,
            caption=caption
        )
    except peewee.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error creating post")

    return {"message": "Post created successfully"}


@app.put("/like_post/{id}")
def like_post(id):
    try:
        likes_info = Like_Table.get(Like_Table.post_id == int(id))
    except Like_Table.DoesNotExist:
        return {"error": "Post not found"}

    likes_info.like_count = likes_info.like_count + 1
    print(likes_info.like_count)
    likes_info.save()
    return {"message": "Liked"}


@app.get("/posts/{username}")
async def get_user_posts(username: str):
    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="User not found")
    
    posts = Post.select().where(Post.user_info == user)
    return [{"post_name": post.post_name, "caption": post.caption} for post in posts]
    
    