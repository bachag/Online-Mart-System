from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from user_service.models import User
from user_service.db import get_session
from user_service.crud import get_user_by_email
from sqlmodel import Session

SECRET_KEY = "your_secret_key"
ALGORITHM="H256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token:str = Depends(oauth2_scheme)):
    credential_expcetion = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate User",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            raise credential_expcetion
    except JWTError:
        raise credential_expcetion
    user = get_user_by_email(session,email=email)
    if user is None:
        raise credential_expcetion
    return user
        
        
        