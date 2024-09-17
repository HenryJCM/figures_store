# services/oci_service.py
import oci
from oci.exceptions import ServiceError
from app.v1.utils.config import settings


class OCIObjectStorageService:
    def __init__(self):
        self.config = oci.config.from_file()
        self.namespace = settings.namespace_name
        self.bucket_name = settings.bucket_name
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
            # Renombrar el objeto en lugar de copiar
            print(f"Renaming object '{old_folder_name}' to '{new_folder_name}'...")
            rename_object_details = oci.object_storage.models.RenameObjectDetails(
                source_name=old_folder_name,
                new_name=new_folder_name
            )

            response = self.client.rename_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                rename_object_details=rename_object_details
            )
            print(f"Successfully renamed object '{old_folder_name}' to '{new_folder_name}'.")

            # Imprimir los encabezados de la respuesta para depuración
            print(response.headers)

        except ServiceError as e:
            if e.status == 404:
                print(f"Object '{old_folder_name}' not found. It may have already been deleted or does not exist.")
            else:
                print(f"Error renaming object '{old_folder_name}' to '{new_folder_name}': {e.message}")
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
                print(f"No objects found with prefix '{folder_name}'. Folder may not exist or already deleted.")
                return  # No hay objetos, por lo tanto, la carpeta no existe o ya fue eliminada

            # Elimina cada objeto en la carpeta
            for obj in list_objects_response.data.objects:
                try:
                    print(f"Deleting object '{obj.name}'...")
                    self.client.delete_object(
                        namespace_name=self.namespace,
                        bucket_name=self.bucket_name,
                        object_name=obj.name
                    )
                    print(f"Successfully deleted object '{obj.name}'.")
                except ServiceError as e:
                    print(f"Error al eliminar el objeto '{obj.name}': {e.message}")

        except ServiceError as e:
            raise Exception(f"Error al eliminar la carpeta en OCI: {e.message}")
