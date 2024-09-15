from typing import List
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.v1.model.model import Sale, User
from app.v1.schema.sale import SaleOut, SaleBase
from app.v1.utils.db import get_db, get_current_user

router = APIRouter()

@router.post('/sale', response_model = SaleOut, dependencies=[Depends(get_current_user)])
def new_sale(sale: SaleBase, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == sale.user_id).one()
    except NoResultFound:
        raise HTTPException(status_code=500, detail=f"Usuario con id {id} no se encuentra en la DB")

    total = 0
    new_sale = Sale(
        id=uuid4(),
        date=user.date,
        user_id=sale,
        total=total,
        sale_details=sale.details,
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale