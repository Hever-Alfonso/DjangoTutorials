from django.core.management.base import BaseCommand

from pages.factories import ProductFactory


class Command(BaseCommand):
    """
    Comando personalizado de Django para poblar la base de datos con productos de prueba.
    Se ejecuta con: python manage.py seed_products
    """

    help = 'Seed the database with products'

    def handle(self, *args, **kwargs):
        # Crea 8 productos falsos usando ProductFactory
        # create_batch(8) llama a la factory 8 veces y guarda cada producto en la BD
        ProductFactory.create_batch(8)

        # Imprime un mensaje de exito en la terminal con formato verde
        self.stdout.write(self.style.SUCCESS('Successfully seeded products'))