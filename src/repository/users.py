

from typing import List
from sqlalchemy import func
import datetime
from sqlalchemy.orm import Session

from src.database.models import User,PhoneNumber,Email
from src.schemas import UserBase,UserMobel,UserResponse

async def get_users(skip: int,limit:int, db:Session) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

async def get_user_by_first_name(name:str,db:Session) -> User:
    return db.query(User).filter(User.first_name == name).first()

async def get_user_by_last_name(name:str,db:Session) -> User:
    
    return db.query(User).filter(User.last_name == name).first()
    
async def get_user_by_email(email:str,db:Session) -> User:
    return db.query(User).join(User.emails).filter(Email.email == email).first()

async def get_users_with_upcoming_birthdays(db: Session) -> List[User]:
    
    
    
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)

    users = db.query(User).filter(
        func.extract('day', User.born_date) >= today.day,
        func.extract('day', User.born_date) <= next_week.day
    ).all()

    return users
        
        
async def create_user(body: UserMobel,db:Session) -> User:
    
    phones = db.query(PhoneNumber).filter(PhoneNumber.id.in_(body.phone_numbers)).all()
    emails = db.query(Email).filter(Email.id.in_(body.emails)).all()
    user = User(first_name=body.first_name,last_name=body.last_name,emails=emails,phone_numbers=phones,born_date=body.born_date)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

async def update_user(user_id: int, body:UserMobel,db:Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        phones = db.query(PhoneNumber).filter(PhoneNumber.id.in_(body.phone_numbers)).all()
        emails = db.query(Email).filter(Email.id.in_(body.emails)).all()
        user.first_name = body.first_name
        user.last_name = body.last_name
        user.emails = emails
        user.phone_numbers = phones
        user.born_date = body.born_date
        db.commit()
    return user  

async def delete_user(user_id:int, body:UserMobel,db:Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


