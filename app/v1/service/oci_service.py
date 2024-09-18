# services/oci_service.py
import oci
from typing import BinaryIO
from oci.exceptions import ServiceError
from app.v1.utils.config import settings


class OCIObjectStorageService:
    def __init__(self):
        self.config = oci.config.from_file()
        self.namespace = settings.namespace_name
        self.bucket_name = settings.bucket_name
        self.bucket_endpoint = settings.bucket_endpoint
        self.client = oci.object_storage.ObjectStorageClient(self.config)

    def create_folder(self, folder_name: str):
        try:
            # Crear una carpeta (objeto con un nombre terminado en '/')
            self.client.put_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                object_name=folder_name,
                put_object_body=b''  # Una carpeta en OCI se crea con un objeto vacío
            )
        except ServiceError as e:
            raise Exception(f"Error al crear la carpeta en OCI: {e.message}")

    def rename_folder(self, old_folder_name: str, new_folder_name: str):
        try:
            # Renombrar el objeto
            print(f"Renombrando objeto '{old_folder_name}' a '{new_folder_name}'...")
            rename_object_details = oci.object_storage.models.RenameObjectDetails(
                source_name=old_folder_name,
                new_name=new_folder_name
            )

            response = self.client.rename_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                rename_object_details=rename_object_details
            )
            print(f"Objeto '{old_folder_name}' renombrado exitosamente a '{new_folder_name}'.")

            # Imprimir los encabezados de la respuesta para depuración
            print(response.headers)

        except ServiceError as e:
            if e.status == 404:
                print(f"Objeto '{old_folder_name}' no encontrado. Podría ya haber sido eliminado o no existir.")
            else:
                print(f"Error al renombrar el objeto '{old_folder_name}' a '{new_folder_name}': {e.message}")
                raise

    def delete_folder(self, folder_name: str):
        try:
            # Lista todos los objetos con el prefijo de la carpeta
            list_objects_response = self.client.list_objects(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                prefix=folder_name
            )

            if not list_objects_response.data.objects:
                print(f"No se encontraron objetos con el prefijo '{folder_name}'. La carpeta podría no existir o ya haber sido eliminada")
                return  # No hay objetos, por lo tanto, la carpeta no existe o ya fue eliminada

            # Elimina cada objeto en la carpeta
            for obj in list_objects_response.data.objects:
                try:
                    print(f"Eliminando objeto '{obj.name}'...")
                    self.client.delete_object(
                        namespace_name=self.namespace,
                        bucket_name=self.bucket_name,
                        object_name=obj.name
                    )
                    print(f"Objeto eliminado exitosamente '{obj.name}'.")
                except ServiceError as e:
                    print(f"Error al eliminar el objeto '{obj.name}': {e.message}")

        except ServiceError as e:
            raise Exception(f"Error deleting folder from OCI: {e.message}")

    def upload_image(self, image_file: BinaryIO, image_filename: str) -> str:
        try:
            content_type = 'image/jpg'
            # Subir el archivo al bucket de OCI
            self.client.put_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                object_name=image_filename,
                put_object_body=image_file,
                content_type=content_type
            )

            # Generar la URL de acceso al objeto
            image_url = f"{self.bucket_endpoint}{image_filename}"
            return image_url
        except Exception as e:
            raise RuntimeError(f"Error uploading image to OCI: {str(e)}")

    def move_image(self, old_path: str, new_path: str):
        try:
            # Descargar la imagen existente
            old_image = self.client.get_object(self.namespace, self.bucket_name, old_path)
            image_data = old_image.data.content

            # Subir la imagen a la nueva ubicación
            self.client.put_object(self.namespace, self.bucket_name, new_path, image_data)

            # Eliminar la imagen antigua
            self.client.delete_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                object_name=old_path  # Se espera el nombre completo del archivo, incluyendo la extensión
            )
        except oci.exceptions.ServiceError as e:
            raise RuntimeError(f"OCI Service error when moving image: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error moving image from OCI: {str(e)}")

    def delete_image(self, image_path: str):
        try:
            self.client.delete_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                object_name=image_path  # Se espera el nombre completo del archivo, incluyendo la extensión
            )
        except oci.exceptions.ServiceError as e:
            raise RuntimeError(f"OCI Service error when deleting image: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error deleting image from OCI: {str(e)}")