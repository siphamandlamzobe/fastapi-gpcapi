
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select
from app.api.dependencies.database import get_db
from app.models.user import User, UserOutput
from starlette import status

security = HTTPBasic()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), session: Session = Depends(get_db)) -> UserOutput:
    query = select(User).where(User.username == credentials.username)
    user = session.exec(query).first()
    if user and user.verify_password(credentials.password):
        return UserOutput.from_orm(user)
    else:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
        )