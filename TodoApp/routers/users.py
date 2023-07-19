from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path,Query
from starlette import status
from models import Users
from db import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext
from models import Users


router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

############## get común ##########################################################
# @router.get('/', status_code=status.HTTP_200_OK)
# async def get_user(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     return db.query(Users).filter(Users.id == user.get('id')).first()



################################################################################### page= la página que se quiere ver
################# get todos con paginado por query ################################ limit= la cantidad de todos por página
################################################################################### por ej: page=2 y limit=5, se verán los todos del 6 al 10, y en la page=1 los 5 primeros

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50), db= Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    query = db.query(Users)
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_users = query[start_index:end_index]

    return paginated_users


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()







