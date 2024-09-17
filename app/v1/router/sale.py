from datetime import datetime
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.v1.model.model import Sale, Cart, SaleDetail, Product
from app.v1.schema.sale import SaleOut
from app.v1.service.mail import send_email
from app.v1.utils.db import get_db, get_current_user

router = APIRouter()

@router.post('/sale', response_model = SaleOut, dependencies=[Depends(get_current_user)])
def new_sale_from_cart(db: Session = Depends(get_db)):
    #Obtenemos el usuario de la sesion
    user = get_current_user(db)

    # Buscamos todos los productos en el carrito de compras
    cart = db.query(Cart).filter(Cart.user_id == user.id).order_by(Cart.date_added.asc())
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario con id {id} no tiene productos en su carrito")

    print(cart)

    new_sale = Sale(
        id=uuid4(),
        date=datetime.now(),
        user_id=user.id
    )
    new_sale.user = user

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

@router.post('/sale/{id}', response_model=SaleOut, dependencies=[Depends(get_current_user)])
def read_sale(id: UUID, db: Session = Depends(get_db)):
    # Encontramos la venta
    try:
        sale = db.query(Sale).filter(Sale.id == id).first()
    except:
        raise HTTPException(status_code=404, detail=f"Venta con id {id} no se encuentra en la DB")

    return sale

@router.post('/sale/{id}/email', dependencies=[Depends(get_current_user)])
def send_sale_to_email(id: UUID, db: Session = Depends(get_db)):
    # Encontramos la venta
    sale = db.query(Sale).filter(Sale.id == id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Venta con el id {id} no existe en la BD")

    success_email = send_email(sale.user.email, "Boleta de Venta - Figures Store","sale", {"sale": sale})

    if success_email:
        return {"detail": f"Se envio el correo con éxito a la dirección {sale.user.email}"}
    else:
        return {"detail": "No se pudo enviar el correo"}
