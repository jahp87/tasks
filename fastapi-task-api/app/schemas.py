from pydantic import BaseModel

class TaskCreate(BaseModel):
    task_name: str
    description: str

class TaskUpdate(BaseModel):
    task_name: str = None
    description: str = None
    status: str = None

class TaskResponse(BaseModel):
    id: int
    task_name: str
    description: str
    status: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None



# Base User schema
class UserBase(BaseModel):
    username: str
    email: str

# Schema for creating a user (requires password)
class UserCreate(UserBase):
    password: str

# Schema for user stored in the database
class UserInDB(UserBase):
    hashed_password: str

# Schema for returning user info (no password)
class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True