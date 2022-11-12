from .. import models,schemas,utils
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"] # to differentiate in documentation between users and post HTTP method
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user : schemas.UserBase ,db: Session = Depends(get_db)):
    
    # hash the password using hash method of CryptoContext 
    hashed_pwd =  utils.hash(user.password)
    user.password = hashed_pwd
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id : int,db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user_ = user_query.first()
    if not user_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} was not found")
    else:
        return user_
