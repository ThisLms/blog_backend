from typing import Literal
from pydantic import BaseModel,Field

class SignupRequest(BaseModel):
    login_id : str = Field(min_length=1, max_length=20)
    password : str = Field(min_length=1, max_length=15)
    user_name : str = Field(min_length=1, max_length=25)
    email : str = Field(min_length=1, max_length=70)
    gender : Literal["",1,2] = ""
    introduction : str = ""
    birthday : str = ""