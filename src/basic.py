from pydantic import BaseModel
from datetime import datetime


#lets create user model , to create a model in pydantic we create a class that inherit from basemodel

class User(BaseModel): #it is mutable and after changing in further code then it wont validate
    uid : int
    username : str
    email : str
    verified_at: datetime|None = None    #default is none and if we need to change to date then we can also do that
    bio:str = ''                             ##we can add optional fiels by seting it default values
    is_active:bool = True
    full_name: str | None = None                 #this is also we can make optional field like making it default because default full name will be none


user = User(
    uid=123,
    username='gagan',
    email='gagan@gmail.com',

)
print(user.username)  #we can use . operator for access , 
print(user.model_dump()) #this gives dictionary
print(user.model_dump_json(indent=2)) # this give json
