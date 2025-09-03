# this file is for our orm to create tavble in mysql database

from sqlalchemy import Boolean, Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'

    id=Column(Integer, primary_key=True,index=True)
    username=Column(String(50),unique=True,index=True)
    hashed_password=Column(String(100))

class Post(Base):
   __tablename__='posts'

   id=Column(Integer, primary_key=True,index=True) 
   title=Column(String(50))
   content=Column(String(100))
   user_id=Column(Integer)