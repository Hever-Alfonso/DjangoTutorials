from abc import ABC, abstractmethod
from django.http import HttpRequest


class ImageStorage(ABC):
    """
    Interfaz abstracta para el almacenamiento de imagenes.

    Define el contrato que deben cumplir todas las implementaciones
    de storage de imagenes (local, S3, Google Cloud, etc.).

    Principio DIP: las vistas dependen de esta abstraccion,
    no de una implementacion concreta como ImageLocalStorage.
    """

    @abstractmethod
    def store(self, request: HttpRequest):
        """
        Guarda la imagen del request y retorna su URL.
        Toda clase que herede de ImageStorage debe implementar este metodo.
        """
        pass