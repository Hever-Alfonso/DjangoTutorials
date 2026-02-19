import factory

from .models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    """
    Factory que genera instancias falsas del modelo Product.
    Usada para poblar la base de datos en desarrollo y pruebas.
    """

    class Meta:
        # Le indica a factory_boy que modelo debe usar para crear los registros
        model = Product

    # Genera un nombre de empresa falso como nombre del producto
    name = factory.Faker('company')

    # Genera un precio entero aleatorio entre 200 y 9000
    price = factory.Faker('random_int', min=200, max=9000)