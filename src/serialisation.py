#basic concept of nstd model is inheritance like class under classs, model under model
import json
from uuid import UUID, uuid4
from pydantic import BaseModel,ValidationError,Field,EmailStr,HttpUrl,SecretStr, field_validator,model_validator,ValidationInfo,computed_field,ConfigDict #configdict is used to configure our model more further
from datetime import UTC, datetime
from functools import partial
from typing import Literal,Annotated  #to add constraints,metadata with type current type

#lets create user model , to create a model in pydantic we create a class that inherit from basemodel

class User(BaseModel): #it is mutable and after changing in further code then it wont validate
    model_config = ConfigDict(populate_by_name=True, strict=True, extra="allow", validate_assignment=True,frozen=True) #,frozen true will froze all the default value after seting you cant change
    # ,validate assignment will revalidate will verify through out after assigning in further code extra allow will allow fields that are not defined in uder model  populate by value gonna accept field name and alias, strict = true gonna stop the conversion of int str to int like that
    uid : UUID = Field(alias = 'id', default_factory=uuid4) #we dont want to put () in end or it will generate only one
    username : Annotated[str, Field(min_length=3,max_length=20)]
    email : EmailStr
    password : SecretStr
    age: Annotated[int, Field(ge=13,le=130)] # ge means greater then or equal to 
    verified_at: datetime|None = None    #default is none and if we need to change to date then we can also do that
    bio:str = ''                             ##we can add optional fiels by seting it default values
    is_active:bool = True
    first_name:str   = ""                #
    last_name:str = ""
    follower_count :int = 0
    website : HttpUrl | None = None
    @field_validator('username') # this is how we make vaidation custom
    @classmethod
    def validate_username(cls, v: str) -> str: 
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v.lower()   ##custom validator works  after pydantic basic checking 
    ### URL Validation (no mode)
    # @field_validator('website')
    # @classmethod
    # def add_https(cls, v: str | None) -> str | None:              #this will also run after the basic checking so method give below is perfect for before checking with before mode
    #     if v and not v.startswith(('http://', 'https://')):
    #         return f'https://{v}'
    #     return v

    ### URL Validation (with mode)
    @field_validator('website', mode="before")
    @classmethod
    def add_https(cls, v: str | None) -> str | None:
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v
    
    @computed_field   
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10000


### Comment Model
class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0
    
class BlogPost(BaseModel):
    title :Annotated[str, Field(min_length=1, max_length=200)]
    content:Annotated[str, Field(min_length=10)]
    author : User   #now here we have the full user object
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
    comments : list[Comment] = Field(default_factory=list)


### Model Validator instead of recieving just values we access self which is the whole model instance and we can access all the field to validations this runs after the
# all the field validations individually thats why we are not using the classmethod
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    
    @model_validator(mode='after')
    def passwords_match(self) -> 'UserRegistration':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match') 
        return self
    

    #bestpractices validator should return value or raise error, usually want to raise value error so pydantic will convert into validation error, 


### BlogPost Dictionary
post_data = {
    "title": "Understanding Pydantic Models",
    "content": "Pydantic makes data validation easy and intuitive...",
    "slug": "understanding-pydantic",
    "author": {
        "username": "coreyms",
        "email": "CoreyMSchafer@gmail.com",
        "age": 39,
        "password": "secret123",
    },
    "comments": [
        {
            "content": "I think I understand nested models now!",   #each comment has to pass comment class format
            "author_email": "student@example.com",
            "likes": 25,
        },
        {
            "content": "Can you cover FastAPI next?",
            "author_email": "viewer@example.com",
            "likes": 15,
        },
    ],
}

# post = BlogPost(**post_data)   #example of kwargs
# there is another way
post = BlogPost.model_validate(post_data)

print(post.model_dump_json(indent=2))

### User Dictionary
user_data = {
    "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",  #here we are passing alias but alias is in code not output
    "username": "Corey_Schafer",
    "email": "CoreyMSchafer@gmail.com",
    "age": 39, #this conversion will stop now cauz of strict if its str
    "password": "secret123",
    "notes": "karen",  # this will be extra field and we can also ristrict this too, ignore
}

user = User.model_validate_json(json.dumps(user_data))  #if we recieving json data from api etc we can manage like this
# print(user.model_dump_json(indent=2, by_alias=True, exclude= {"password"}))         #by alias = true gonaa provide the alias name in output, exclude will exdlude the specific field
# print(user.model_dump_json(indent=2, include={"username", "email"}))  #include will include the specific data
print(user.model_dump_json(indent=2))