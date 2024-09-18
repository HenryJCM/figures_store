from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.v1.schema.brand import ProductCreate, ProductResponse
from app.v1.model.model import Product, Brand
from app.v1.service.oci_service import OCIObjectStorageService
from app.v1.utils.db import get_db, get_current_user
from typing import List
import logging
from uuid import uuid4, UUID

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

# Crear una instancia del servicio OCI
oci_service = OCIObjectStorageService()


@router.post("/add_product", response_model=ProductResponse, dependencies=[Depends(get_current_user)])
def create_product(
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...),
        brand_id: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    try:
        # Generar un ID único para el producto
        product_id = uuid4()

        # Obtener el nombre de la marca desde el ID de la marca
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
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

    return JSONResponse(content={"message": f"New product '{name}' registered successfully."}, status_code=200)