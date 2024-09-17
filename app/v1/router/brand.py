from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.v1.schema.brand import BrandCreate, BrandResponse
from app.v1.model.model import Brand
from app.v1.service.oci_service import OCIObjectStorageService
from app.v1.utils.db import get_db, get_current_user
from typing import List
import logging
from uuid import uuid4, UUID

router = APIRouter()
logger = logging.getLogger("uvicorn.error")
# Crear una instancia del servicio OCI
oci_service = OCIObjectStorageService()


@router.post("/add_brand", response_model=BrandResponse, dependencies=[Depends(get_current_user)])
def register_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    try:
        db_brand = Brand(id=uuid4(), name=brand.name)
        # Registrar la marca en la base de datos
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        # Crear una carpeta (objeto con un nombre terminado en '/')
        folder_name = f"{brand.name}/"  # El nombre de la carpeta debe terminar con '/'
        oci_service.create_folder(folder_name)
    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"message": f"Marca '{brand.name}' registrada correctamente."}, status_code=200)


@router.get("/all_brands/", response_model=List[BrandResponse], dependencies=[Depends(get_current_user)])
def get_brands(db: Session = Depends(get_db)):
    try:
        # Obtener todas las marcas
        brands = db.query(Brand).all()
        return brands

    except Exception as e:
        # Maneja cualquier otro tipo de excepción y devuelve un error 500
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/brand/{id}", response_model=BrandResponse, dependencies=[Depends(get_current_user)])
def get_brand_by_id(id: UUID, db: Session = Depends(get_db)):
    try:
        if id is not None:
            # Obtener una marca específica por ID
            brand = db.query(Brand).filter(Brand.id == id).first()
            if brand is None:
                raise HTTPException(status_code=404, detail="Marca no encontrada.")
            return brand
        else:
            # Obtener todas las marcas
            brands = db.query(Brand).all()
            return brands

    except HTTPException as http_exc:
        # Maneja específicamente las excepciones HTTP para evitar errores 500 inesperados
        # logger.warning(f"HTTPException: {http_exc.detail}", exc_info=True)
        raise http_exc

    except Exception as e:
        # Maneja cualquier otro tipo de excepción y devuelve un error 500
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.put("/update_brand/{brand_id}", response_model=BrandResponse, dependencies=[Depends(get_current_user)])
def update_brand(brand_id: UUID, brand: BrandCreate, db: Session = Depends(get_db)):
    try:
        # Obtener la marca existente
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not db_brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada.")

        # Actualizar el nombre en la base de datos
        old_name = db_brand.name
        db_brand.name = brand.name
        db.commit()
        db.refresh(db_brand)

        # Renombrar la carpeta en OCI
        old_folder_name = f"{old_name}/"
        new_folder_name = f"{brand.name}/"
        oci_service.rename_folder(old_folder_name, new_folder_name)

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"message": f"Marca '{old_name}' actualizada a '{brand.name}' exitosamente."}, status_code=200)


@router.delete("/delete_brand/{brand_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user)])
def delete_brand(brand_id: UUID, db: Session = Depends(get_db)):
    try:
        # Obtener la marca existente
        db_brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not db_brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada")

        # Obtener el nombre de la marca
        brand_name = db_brand.name

        # Eliminar la marca de la base de datos
        db.delete(db_brand)
        db.commit()

        # Eliminar la carpeta en OCI
        folder_name = f"{brand_name}/"
        oci_service.delete_folder(folder_name)

    except Exception as e:
        db.rollback()  # Rollback en caso de error
        raise HTTPException(status_code=500, detail=str(e))

    return JSONResponse(content={"message": f"Marca '{brand_name}' eliminada exitosamente."}, status_code=200)