from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from user_service.db import create_db_and_tables, get_session
from user_service.schemas import UserCreate, UserRead, TokenResponse, UserDataCreate, UserDataRead, TokenData
from user_service.crud import create_user, get_user_by_email, authenticate_user, create_user_data, get_user_data, refresh_access_token, validate_password
from user_service.auth import create_access_token
from user_service.dp import get_current_user
from user_service.models import User, UserData
from contextlib import asynccontextmanager
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List
import asyncio
from user_service.kafka.producer import 
from user_service.kafka.consumer import run_consumer



limiter = Limiter(key_func=get_remote_address)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    consumer_task = create_task(run_consumer())
    try:
        yield
    finally:
        consumer_task.cancel()

app:FastAPI = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hwllo", "World"}

@app.post("/register",response_model=UserRead)
async def register_user(user:UserCreate,db=Depends(get_session)):
    db_user = get_user_by_email(db,user.email)
    if db_user:
        raise HTTPException(status_code=400,detail="Emaill already exist")
    if not validate_password(user.password):
        raise HTTPException(status_code=400,detail="Password doesnjot match criteria")
    new_user = create_user(session=db,user=user)
    return new_user
@app.get("/user/me",response_model=UserRead)
def read_user_me(current_user:User = Depends(get_current_user)):
    return current_user
@app.post("/data",response_model=UserDataRead)
async def create_new_data_endpoint(data:UserDataCreate,current = Depends(get_current_user),db:Session=Depends(get_session)):
    new_user_data = create_user_data(session=db,data=data,user=current)
    return new_user_data

@app.get("/data",response_model=List[UserDataRead])
def read_user_data(current_user:User= Depends(get_current_user),db:Session = Depends(get_session)):
    return get_user_data(session=db,user=current_user)
@app.post("/token",response_model=TokenResponse)
@limiter.limit("5 per minute")
def login_user(request:Request,  form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_session)):
    user = authenticate_user(session=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credential")
    access_token = create_access_token(data={"sub":user.email})
    return {"access_token":access_token,"token_type":"bearer"}
@app.post("/refresh",response_model=TokenResponse)
def refresh_token(token:TokenData,db:Session=Depends(get_session)):
    new_token = refresh_access_token(token=token.access_token,db=db)
    if not new_token:
        raise HTTPException(status_code=400, detail="Invalid Toekn")
    return {"access_token":new_token,"token_type":"bearer"}
    




