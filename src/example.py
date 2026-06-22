#unlike dataclass , our base model provides us validation in run time\
from pydantic import BaseModel

class User(BaseModel):
    username : str
    email:str
    age:int


user1 = User(username='gagan', email='gagan@gmail.com', age=38)
print(user1)

user2 = User(username='gangan', email=None, age="old")   #here you go you can see error here
print(user2)