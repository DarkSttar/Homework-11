from typing import List

from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.schemas import UserBase,UserMobel,UserResponse
from src.repository import users as repository_users

router = APIRouter(prefix='/users',tags=['users'])



@router.get('/', response_model=List[UserResponse])
async def read_user(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    users = await repository_users.get_users(skip,limit,db)
    return users

@router.get('/upcomingbirthdays', response_model=List[UserResponse])
async def read_users_with_upcoming_birthdays(db:Session = Depends(get_db)):
    users = await repository_users.get_users_with_upcoming_birthdays(db)
    return users
@router.get('/firstname/{first_name}', response_model=UserResponse)
async def read_user_by_first_name(first_name:str,db:Session = Depends(get_db)):
    user = await repository_users.get_user_by_first_name(first_name,db)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user

@router.get('/lastname/{name}',response_model=UserResponse)
async def read_user_by_last_name(name:str, db:Session = Depends(get_db)):
    user = await repository_users.get_user_by_last_name(name,db)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user

@router.get('/email/{email}',response_model=UserResponse)
async def read_user_by_email(email:str,db:Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(email,db)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user
@router.post('/',response_model=UserResponse)
async def create_user(body:UserMobel,db: Session = Depends(get_db)):
    user = await repository_users.create_user(body,db)
    return user


@router.put('/{user_id}',response_model=UserResponse)
async def update_user(user_id:int,body:UserMobel,db: Session = Depends(get_db)):
    user = await repository_users.update_user(user_id,body,db)
    if user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User Not Found')
    return user

@router.delete('/{user_id}',response_model=UserResponse)
async def remove_user(user_id:int, body:UserResponse,db: Session = Depends(get_db)):
    user = await repository_users.delete_user(user_id,body,db)
    if user is None:
        HTTPException(status_code=status.Http_404,detail='User not found')
    return user