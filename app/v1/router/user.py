from typing import List
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.v1.model.model import User
from app.v1.schema.schema import UserOut, UserCreate
from app.v1.utils.db import get_db, get_password_hash, get_current_user

router = APIRouter()

@router.post('/user', response_model = UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)

    new_user = User(
        id=uuid4(),
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/all_users", response_model=List[UserOut], dependencies=[Depends(get_current_user)])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()   # Obtenemos todos los usuarios

# API protegida por el token
@router.get("/user/{id}", response_model=UserOut, dependencies=[Depends(get_current_user)])
def read_user(id: UUID, session: Session = Depends(get_db)):
    user = session.query(User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no se encuentra en la DB")

    return user

#@router.put("/user/{id}", response_model=UserOut)
#def update_user(id: UUID, user_update: UserCreate, session: Session = Depends(get_db)):
#    user = session.query(User).get(id)
#
#    if user:
#        user.first_name = user_update.first_name
#        user.last_name = user_update.last_name
#        user.address = user_update.address
#        user.email = user_update.email
#        session.commit()
#
#    if not user:
#        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no fue encontrado para actualizar")
#
#    return user
#
#@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
#def delete_user(id: UUID, session: Session = Depends(get_db)):
#    user = session.query(User).get(id)
#
#    if user:
#        session.delete(user)
#        session.commit()
#
#    if not user:
#        raise HTTPException(status_code=404, detail=f"Usuario con id {id} no fue encontrado")
#
#    return user