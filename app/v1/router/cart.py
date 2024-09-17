from datetime import datetime
from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.v1.model.model import Cart, Product, User
from app.v1.schema.cart import CartOut, CartBase, CartListBase, CartUpdate
from app.v1.utils.db import get_db, get_current_user, require_role

router = APIRouter()

@router.post('/cart', response_model = CartOut, dependencies=[Depends(get_current_user)])
async def add_product_to_cart(cart: CartBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Validar el stock del producto
    try:
        product = db.query(Product).filter(Product.id == cart.product_id).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con id {cart.product_id} no existe")

    if product.stock <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto con id {cart.product_id} no tiene stock suficiente")

    # Buscar si ya existe un registro en el carrito con el mismo producto
    new_cart = None
    try:
        new_cart = db.query(Cart).filter(Cart.product_id == cart.product_id and Cart.user_id == current_user.id).one()
    except NoResultFound:
        pass

    # Crear el registo si no existe
    if not new_cart:
        new_cart = Cart(
            id=uuid4(),
            quantity=1,
            date_added=datetime.now(),
            user_id=current_user.id
        )

        new_cart.user = current_user
        new_cart.product = product
    # utilizar el registro existente
    else:
        new_cart.quantity = new_cart.quantity + 1

    product.stock = product.stock - 1

    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

@router.get('/cart', response_model=CartListBase, dependencies=[Depends(get_current_user)])
def read_cart_by_current_user( db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    # Buscamos todos los productos en el carrito de compras
    carts = db.query(Cart).filter(Cart.user_id == current_user.id).order_by(Cart.date_added.asc())
    if not carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {current_user.id} no tiene productos en su carrito")

    return CartListBase(items=carts)

@router.put('/cart/{id}', response_model = CartOut, dependencies=[Depends(get_current_user)])
async def update_cart(id: UUID, cart_update: CartUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart = db.query(Cart).get(id)

    ## validar cantidad

    if cart:
        cart.quantity = cart_update.quantity
        db.commit()

    if not cart:
        raise HTTPException(status_code=404, detail=f"Detalle del carrito de compras con id {id} no fue encontrado para actualizar")

    return cart

@router.delete('/cart/{id}', response_model = CartOut, dependencies=[Depends(get_current_user)])
async def delete_cart(id: UUID, db: Session = Depends(get_db)):
    cart = db.query(Cart).get(id)

    if cart:
        db.delete(cart)
        db.commit()

    if not cart:
        raise HTTPException(status_code=404, detail=f"Detalle del carrito de compras con id {id} no fue encontrado")

    return cart