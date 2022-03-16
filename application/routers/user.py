from fastapi import status, Depends , HTTPException, Response, APIRouter
from .. import models, schemas, utils
from typing import List #, Optional
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def createUser(user: schemas.UserCreate,db: Session = Depends(get_db) ):
    #hash the password
    
    hashed_password = utils.hashed(user.password)
    user.password = hashed_password
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{identifier}", status_code = status.HTTP_204_NO_CONTENT)
def deleteUser(identifier: int,db: Session = Depends(get_db)):
    response = db.query(models.User).filter(models.Post.id == identifier)
    if response.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {identifier} is not accessible")

    response.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/", response_model= List[schemas.UserOut])
def getUsers(db: Session = Depends(get_db)):    
    users = db.query(models.User).all()
    
    return users

@router.get("/{identifier}", response_model= schemas.UserOut)
def getSpecificUser(identifier: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == identifier).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {identifier} is not accessible")
    
    return user