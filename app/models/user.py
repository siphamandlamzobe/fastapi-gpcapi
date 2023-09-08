from sqlmodel import Field, SQLModel, Column, VARCHAR
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""
    
    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
class UserOutput(SQLModel):
    id: int
    username: str   
    
    