from fastapi import FastAPI, File, UploadFile
from peewee import*
from typing import Union

DATABASE = 'tweepee3.db'

database = SqliteDatabase(DATABASE)


#model definitions -- the standard "pattern" is to define a base model class
#that specifies which database to use then, any subclass will auomaically use the correct sorage. for main information, see:
# https://charlesleifer.com/docs/peewee/peewee/models.html#models-api-smells-like-django

class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(unique = True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

class Post(BaseModel):
    text = CharField()
    location = CharField()
    date_posted = DateTimeField()
    user = ForeignKeyField(User, backref='posts')

class Likes(BaseModel):
    number_of_likes = IntegerField()
    user = ForeignKeyField(User, backref='liked_user')
    post = ForeignKeyField(Post, backref='liked_post')

#simple utility function to create tables
# def create_tables():
#     with database:
#         database.create_tables([User, Post, Likes])

#allow running from the command line
# if __name__ == '__main__':
#     create_tables()

# brew install --cask db-browser-for-sqlite

# user1 = User.create(username = 'Vaibhav', password = '1234' , email='vk@gmail.com'   , join_date='30/01/2023')
# user2 = User.create(username = 'Aman'   , password = 'xyzuc', email='ak@gmail.com'   , join_date='30/01/2023')
# user3 = User.create(username = 'Akash'  , password = 'dwcjv', email='akash@gmail.com', join_date='30/01/2023')
# user4 = User.create(username = 'Sahil'  , password = 'wdv'  , email='sahil@gmail.com', join_date='30/01/2023')
# user5 = User.create(username = 'Vipul'  , password = 'eckj' , email='vipul@gmail.com', join_date='30/01/2023')

# post1 = Post.create(text = 'Hey There', location='Mumbai', date_posted='30/01/2022', user = user1)
# post2 = Post.create(text = 'Hello ', location='Mumbai', date_posted='30/01/2022', user = user2)
# post3 = Post.create(text = 'fkj ', location='Alahabad', date_posted='30/01/2022', user = user3)
# post4 = Post.create(text = 'cdkjwc ', location='Lucknow', date_posted='30/01/2022', user = user3)
# post5 = Post.create(text = 'dcjk ', location='Guwahati', date_posted='30/01/2022', user = user1)

# like1 = Likes.create(number_of_likes = 20, user = user1, post = post1)
# like2 = Likes.create(number_of_likes = 50, user = user1, post = post5)
# like3 = Likes.create(number_of_likes = 10, user = user3, post = post3)
# like4 = Likes.create(number_of_likes = 60, user = user3, post = post4)
# like5 = Likes.create(number_of_likes = 40, user = user2, post = post2)


# for posts in Post.select().where(Post.user_id == 1):
#     print(posts.text,',',posts.location)

# print(Post.select().where(Post.user_id == 1))
# print(Likes.select().where(post_id = 1))
app = FastAPI()

@app.get("/like/{postID}")

def like(postID):
    postLike = Likes.get(Likes.post_id == int(postID))
    postLike.number_of_likes = postLike.number_of_likes + 1
    postLike.save()
    return {"Success"}

@app.get("/dislike/{postID}")

def dislike(postID):
    postLike = Likes.get(Likes.post_id == int(postID))
    postLike.number_of_likes = postLike.number_of_likes - 1
    postLike.save()
    return {"Success"}


@app.get("/delete/{postID}")

def delete(postID):
    toBeDeleted = Post.get(id == int(postID))
    toBeDeleted.delete_instance()
    return {"Success"}

@app.get("/limitPost")

def limitPost(limit : int = None):
    # return Post.select(Post.text).limit(n)
    query = Post.select()

    if limit:
        query = query.limit(limit)
    
    return [{"user_id":post.text} for post in query]

@app.get("/filterUserName")

def filterUserName(username : str):
    # return Post.select(Post.text).limit(n)
    query = User.get(User.username.contains(username))
    
    return query


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}