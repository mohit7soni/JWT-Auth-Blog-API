from fastapi import FastAPI, Depends,HTTPException,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import auth

app = FastAPI()

app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
    username: str


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

db_dependency = Annotated[Session, Depends(lambda: SessionLocal())]

def get_db():  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#for authentication
app.get("/", status_code=status.HTTP_200_OK)
async def user(user:None, db: db_dependency):
  if user is None:
    raise HTTPException(status_code=401, detail="Unauthorized") 
    return {"uSER":user}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK) 
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post   




#for users

@app.post("/users/")
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "user created successfully"}

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # ✅ Corrected this line