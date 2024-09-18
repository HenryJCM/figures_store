from datetime import datetime
from typing import List
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.v1.model.model import Sale, Cart, SaleDetail, Product, User
from app.v1.schema.sale import SaleOut
from app.v1.service.mail import send_email
from app.v1.utils.db import get_db, get_current_user

router = APIRouter()

@router.post('/sale', response_model = SaleOut, dependencies=[Depends(get_current_user)])
def new_sale_from_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Buscamos todos los productos en el carrito de compras
    cart = db.query(Cart).filter(Cart.client_id == current_user.id).order_by(Cart.date_added.asc())
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con id {id} no tiene productos en su carrito")

    new_sale = Sale(
        id=uuid4(),
        date=datetime.now(),
        client_id=current_user.id
    )
    new_sale.client = current_user

    details = []
    for item in cart:
        # Encontramos el producto
        product = db.query(Product).filter(Product.id == item.product_id).one()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con id {id} no existe")

        detail = SaleDetail(
            id=uuid4(),
            sale_id=new_sale.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price
        )

        detail.sale = new_sale
        detail.product = product
        details.append(detail)

        # Eliminamos los productos del carrito
        db.delete(item)

    new_sale.sale_details = details
    new_sale.calculate_total()

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale

@router.get('/all_sales', response_model=List[SaleOut], dependencies=[Depends(get_current_user)])
def list_sales(db: Session = Depends(get_db)):
    # Encontramos las compras
    sales = db.query(Sale).all()

    return sales

@router.get('/sale/{id}', response_model=SaleOut, dependencies=[Depends(get_current_user)])
def read_sale(id: UUID, db: Session = Depends(get_db)):
    # Encontramos la compra
    sale = db.query(Sale).filter(Sale.id == id).first()

    if not sale:
        raise HTTPException(status_code=404, detail=f"Compra con id {id} no se encuentra en la DB")

    return sale

@router.delete('/sale/{id}', response_model=SaleOut, dependencies=[Depends(get_current_user)])
def delete_sale(id: UUID, db: Session = Depends(get_db)):
    # Encontramos la compra
    sale = db.query(Sale).filter(Sale.id == id).first()

    if sale:
        # devolver stock de todos los items
        for detail in sale.sale_details:
            detail.product.stock += detail.quantity

        #eliminamos la compra
        db.delete(sale)
        db.commit()

    if not sale:
        raise HTTPException(status_code=404, detail=f"Compra con id {id} no se encuentra en la DB")

    return sale

@router.put('/sale/{id}/email', dependencies=[Depends(get_current_user)])
async def send_sale_to_email(request: Request, id: UUID, db: Session = Depends(get_db)):
    # Encontramos la compra
    sale = db.query(Sale).filter(Sale.id == id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Compra con el id {id} no existe en la BD")

    success_email = await send_email(sale.client.email, "Boleta de Venta - Figures Store","sale", {"request": request, "sale": sale})

    if success_email:
        return {"detail": f"Se envio el correo con éxito a la dirección {sale.client.email}"}
    else:
        return {"detail": "No se pudo enviar el correo"}
