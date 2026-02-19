from django.db import models


class Product(models.Model):
    """
    Modelo que representa un producto en la tienda en linea.
    Genera la tabla 'pages_product' en la base de datos.
    """

    # Nombre del producto, maximo 255 caracteres
    name = models.CharField(max_length=255)

    # Precio del producto en numero entero, sin decimales
    price = models.IntegerField()

    # Fecha y hora de creacion, se asigna automaticamente al crear el registro
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha y hora de ultima modificacion, se actualiza automaticamente al guardar
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """
    Modelo que representa un comentario asociado a un producto.
    Genera la tabla 'pages_comment' en la base de datos.
    Un producto puede tener muchos comentarios (relacion uno a muchos).
    """

    # ForeignKey crea la relacion con Product.
    # on_delete=CASCADE significa que si se borra el producto,
    # todos sus comentarios se borran automaticamente tambien.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Texto del comentario, sin limite de caracteres (TextField)
    description = models.TextField()