from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.v1.schema.product import ProductUpdate, ProductResponse, ProductBrandUpdate
from app.v1.model.model import Product, Brand
from app.v1.service.oci_service import OCIObjectStorageService
from app.v1.utils.db import get_db, require_role, get_current_user
from typing import List
import logging
from uuid import uuid4, UUID

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

# Crear una instancia del servicio OCI
oci_service = OCIObjectStorageService()


@router.post("/add_product/", response_model=ProductResponse, dependencies=[Depends(require_role("admin"))])
def register_product(
        name: str = Form(...),
        description: str = Form(None),
        price: float = Form(...),
        stock: int = Form(...),
        brand_id: UUID = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        # Verificar si el nombre del producto ya existe en la misma marca
        existing_product = db.query(Product).filter(
            Product.name == name,
            Product.brand_id == brand_id
        ).first()

        if existing_product:
            raise HTTPException(status_code=400, detail="El nombre del producto ya existe en esta marca.")

        # Generar un ID único para el producto
        product_id = uuid4()

        # Obtener el nombre de la marca desde el ID de la marca
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada.")
        brand_name = brand.name

        # Crear el producto en la base de datos
        db_product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            image_url='',
            stock=stock,
            brand_id=brand_id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        # Generar el nombre del archivo de imagen basado en el ID del producto
        image_filename = f"{product_id}.jpg"

        # Definir el path completo en el bucket de OCI
        oci_image_path = f"{brand_name}/{image_filename}"

        # Subir la imagen al bucket de OCI y obtener la URL
        image_url = oci_service.upload_image(image.file, oci_image_path)

        # Actualizar la URL de la imagen en la base de datos
        db_product.image_url = image_url
        db.commit()
        db.refresh(db_product)

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(
        content={"message": f"Nuevo producto '{name}' registrado exitosamente con url de imagen: '{image_url}'."},
        status_code=200)


@router.get("/all_products", response_model=List[ProductResponse], dependencies=[Depends(get_current_user)])
def get_products(db: Session = Depends(get_db)):
    try:
        # Obtener todos los productos
        products = db.query(Product).all()
        return products

    except Exception as e:
        # Maneja cualquier otro tipo de excepción y devuelve un error 500
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/product/{id}", dependencies=[Depends(get_current_user)])
def read_product(id: UUID, db: Session = Depends(get_db)):
    product = db.query(Product).get(id)

    if not product:
        raise HTTPException(status_code=404, detail=f"Producto con id {id} no se encuentra en DB")

    # Obtener la marca asociada al producto
    brand = db.query(Brand).filter(Brand.id == product.brand_id).first()
    brand_name = brand.name if brand else None

    # Preparar la respuesta con el nombre de la marca
    response = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "image_url": product.image_url,
        "stock": product.stock,
        "brand_id": product.brand_id,
        "brand_name": brand_name  # Añadir el nombre de la marca
    }

    return response


@router.put("/update_product/{id}", response_model=ProductResponse, dependencies=[Depends(require_role("admin"))])
def update_product(id: UUID, product_update: ProductUpdate, db: Session = Depends(get_db)):
    try:
        # Obtener el producto de la base de datos
        product = db.query(Product).get(id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Actualizar los campos del producto
        product.name = product_update.name
        product.description = product_update.description
        product.price = product_update.price
        product.stock = product_update.stock

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(product)

        return product

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/change_product_brand/{product_id}", dependencies=[Depends(require_role("admin"))])
def change_product_brand(product_id: UUID, change_brand: ProductBrandUpdate, db: Session = Depends(get_db)):
    try:
        # Obtener el producto de la base de datos
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")

        # Obtener la marca actual y la nueva
        current_brand = db.query(Brand).filter(Brand.id == product.brand_id).first()
        new_brand = db.query(Brand).filter(Brand.id == change_brand.brand_id).first()
        if not new_brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada.")

        # Construir las rutas de las imágenes
        old_image_path = f"{current_brand.name}/{product.id}.jpg"
        new_image_path = f"{new_brand.name}/{product.id}.jpg"

        # Mover la imagen en OCI
        oci_service.move_image(old_image_path, new_image_path)

        # Actualizar el brand_id en la base de datos
        product.brand_id = change_brand.brand_id

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(product)

        return {"message": f"Marca para producto '{product.name}' cambiada exitosamente."}

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_product_image/{product_id}", dependencies=[Depends(require_role("admin"))])
async def update_product_image(product_id: UUID, image: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Obtener el producto de la base de datos
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Obtener la marca actual
        current_brand = db.query(Brand).filter(Brand.id == product.brand_id).first()

        # Construir la ruta de la nueva imagen usando el ID del producto
        image_path = f"{current_brand.name}/{product_id}.jpg"  # Asegúrate de usar la extensión correcta

        # Eliminar la imagen antigua
        oci_service.delete_image(image_path)

        # Subir la nueva imagen y actualizar la URL de la imagen en la base de datos
        image_data = await image.read()  # Leer el contenido de la nueva imagen
        product.image_url = oci_service.upload_image(image_data, image_path)

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(product)

        return {"message": f"Imagen para producto '{product.name}' actualizada exitosamente."}

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_product/{product_id}", response_model=dict, dependencies=[Depends(require_role("admin"))])
def delete_product(product_id: str, db: Session = Depends(get_db)):
    try:
        # Obtener el producto de la base de datos
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Obtener el nombre de la marca
        brand = db.query(Brand).filter(Brand.id == product.brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

        # Eliminar el producto de la base de datos
        db.delete(product)
        db.commit()

        # Eliminar la imagen del bucket de OCI
        image_filename = f"{product_id}.jpg"  # Asegúrate de usar la extensión correcta
        image_path = f"{brand.name}/{image_filename}"  # Carpeta de la marca
        oci_service.delete_image(image_path)  # Eliminar la imagen usando la ruta completa

        return {"message": f"Producto '{product.name}' y su imagen eliminados exitosamente."}

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))