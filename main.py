from fastapi import FastAPI
from peewee import*

DATABASE = 'tweepee2.db'

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

#simple utility function to create tables
# def create_tables():
#     with database:
#         database.create_tables([User, Post])

#allow running from the command line
# if __name__ == '__main__':
#     create_tables()

# brew install --cask db-browser-for-sqlite

# user1 = User.create(username = 'Vaibhav', password = '1234' , email='vk@gmail.com'   , join_date='30/01/2023')
# user2 = User.create(username = 'Aman'   , password = 'xyzuc', email='ak@gmail.com'   , join_date='30/01/2023')
# user3 = User.create(username = 'Akash'  , password = 'dwcjv', email='akash@gmail.com', join_date='30/01/2023')
# user4 = User.create(username = 'Sahil'  , password = 'wdv'  , email='sahil@gmail.com', join_date='30/01/2023')
# user5 = User.create(username = 'Vipul'  , password = 'eckj' , email='vipul@gmail.com', join_date='30/01/2023')

# Post.create(text = 'Hey There', location='Mumbai', date_posted='30/01/2022', user = user1)
# Post.create(text = 'Hello ', location='Mumbai', date_posted='30/01/2022', user = user2)
# Post.create(text = 'fkj ', location='Alahabad', date_posted='30/01/2022', user = user3)
# Post.create(text = 'cdkjwc ', location='Lucknow', date_posted='30/01/2022', user = user3)
# Post.create(text = 'dcjk ', location='Guwahati', date_posted='30/01/2022', user = user1)

# for posts in Post.select().where(Post.user_id == 1):
#     print(posts.text,',',posts.location)

# print(Post.select().where(Post.user_id == 1))



app = FastAPI()

@app.get("/")

def read_root():
    return{"Hello": "World"}

@app.get("/getUser")

def getUser():
    k = User.select()
    ans = []

    for i in k:
        ans.append(i)
    return ans

@app.get("/getSingleUser/{name}")

def getSingleUser(name):
    # k = User.select()
    # ans = []

    # for i in k:
    #     if i.username == userName:
    #         ans.append(i)
    # return ans
    ans=[]
    ans = User.get(name == User.username)
    return ans

@app.get("/getPost")

def getPost():
    k = Post.select()
    ans = []

    for i in k:
        ans.append(i)
    return ans

@app.get("/getPostById/{userID}")

def getPostById(userID : int):
    k = Post.select()
    ans = []

    for i in k:
        if i.user_id == userID:
            ans.append(i)
    return ans