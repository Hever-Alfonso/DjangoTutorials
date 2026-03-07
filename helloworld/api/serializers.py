from rest_framework import serializers
from pages.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # ReadOnlyField: estos campos no se pueden enviar desde la API.
    # Django los asigna automaticamente:
    # - created_at: se asigna una sola vez al crear el registro (auto_now_add=True)
    # - updated_at: se actualiza automaticamente cada vez que se guarda (auto_now=True)
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        # Le indica a DRF que modelo usar para generar el serializer
        model = Product
        # Solo estos campos aparecen en el JSON de respuesta y request.
        # El serializer convierte instancias de Product a este formato JSON:
        # {
        #   "id": 1,
        #   "name": "Tv Samsung",
        #   "price": 1000,
        #   "created_at": "2026-03-07T...",
        #   "updated_at": "2026-03-07T..."
        # }
        fields = ['id', 'name', 'price', 'created_at', 'updated_at']