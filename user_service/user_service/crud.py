import jwt
from sqlmodel import Session,select
from user_service.models import User,UserData
from user_service.schemas import UserCreate
from typing import Optional,List
from user_service.auth import ALGORITHM,SECRET_KEY,create_access_token,get_password_hash,verify_password
from user_service.schemas import UserCreate,UserDataCreate
import re
from  jwt import PyJWTError

def get_user_by_email(session:Session,email:str)->Optional[User]:
    statment = select(User).where(User.email == email)
    return session.exec(statment).first()
def create_user(session:Session,user:UserCreate)->User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email,hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
def create_user_data(session: Session, data: UserDataCreate, user: User) -> UserData:
    user_data = UserData(data=data.data, owner_id=user.id)  # Extract 'data' field from UserDataCreate
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data
def authenticate_user(session:Session,email:str,password:str):
    user = get_user_by_email(session,email=email)
    if not user or  not verify_password(password,user.hashed_password):
        return None
    return user
def get_user_data(session:Session,user:User)->List[UserData]:
    statment = select(UserData).where(UserData.owner_id == user.id)
    return session.exec(statment).all()
def validate_password(password: str) -> bool:
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'
    return bool(re.match(pattern, password))

    
def refresh_access_token(token:str,db:Session)->str:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            return None
        user= get_user_by_email(db,email)
        if user is None:
            return None
        return create_access_token(data={"sub":user.email})
    except:
        return None