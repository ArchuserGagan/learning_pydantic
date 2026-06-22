from pydantic import BaseModel,ValidationError,Field
from datetime import UTC, datetime
from functools import partial
from typing import Literal,Annotated  #to add constraints,metadata with type current type

#lets create user model , to create a model in pydantic we create a class that inherit from basemodel

class User(BaseModel): #it is mutable and after changing in further code then it wont validate
    uid : Annotated[int, Field(gt=0)] #here we add the type of data it accept and the constraint of greater then 0
    username : Annotated[str, Field(min_length=3,max_length=20)]
    email : str
    age: Annotated[int, Field(ge=13,le=130)] # ge means greater then or equal to 
    verified_at: datetime|None = None    #default is none and if we need to change to date then we can also do that
    bio:str = ''                             ##we can add optional fiels by seting it default values
    is_active:bool = True
    full_name: str | None = None                #this is also we can make optional field like making it default because default full name will be none



class BlogPost(BaseModel):
    title :Annotated[str, Field(min_length=1, max_length=200)]
    content:Annotated[str, Field(min_length=10)]
    author_id : str | int
    view_count: int = 0
    is_published: bool = False

    tags: list[str] = Field(default_factory=list) #default factory is func is used create a default new value each time you call an instance
    # we can use empty list in pydantic too, but its bad habbit

    # created_at: datetime = datetime.now(UTC) # this wouldnt work it will only work when class is defined not when each time we create an instance so time willbecome instant
    # created_at: datetime = Field(default_factory=datetime.now(tz=UTC)) #still we are calling the func
    ## created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC)) #lambda is an anonymus func now it will work each time when instance will call
    #there is another way to get unexecuted function by using functools partial

    created_at : datetime = Field(default_factory= partial(datetime.now, tz=UTC)) #passing func and argument
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]  #regular expression different concept


### Invalid User
try:
    user = User(
        uid=0,
        username="cs",
        email="CoreyMSchafer@gmail.com",
        age=12,
    )
except ValidationError as e:
    print(e)


# ### New BlogPost
# post = BlogPost(
#     title="Getting Started with Python",
#     content="Here's how to begin...",
#     author_id="12345",
# )

# print(post)