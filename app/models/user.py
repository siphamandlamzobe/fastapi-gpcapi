from sqlmodel import Field, SQLModel, Column, VARCHAR

class User(SQLModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

    
class UserOutput(SQLModel):
    id: int
    username: str   
    
    