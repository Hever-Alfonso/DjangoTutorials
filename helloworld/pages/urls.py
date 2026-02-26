from django.urls import path

# Importamos todas las vistas necesarias
from .views import (
    HomePageView,
    AboutPageView,
    ContactPageView,
    ProductIndexView,
    ProductShowView,
    ProductCreateView,
    ProductCreatedView,
    CartView,
    CartRemoveAllView,
    ImageViewFactory,
    ImageViewNoDI,
)

# Importamos la implementacion concreta de storage para inyectarla en las rutas
# Aqui ocurre la INYECCION DE DEPENDENCIAS:
# Le pasamos ImageLocalStorage() a ImageViewFactory en el momento de definir las rutas
from .utils import ImageLocalStorage

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('products/', ProductIndexView.as_view(), name='index'),
    path('products/create', ProductCreateView.as_view(), name='form'),
    # Ruta de confirmacion: se activa despues de guardar un producto exitosamente
    path('products/create/success', ProductCreatedView.as_view(), name='product-created'),
    path('products/<str:id>', ProductShowView.as_view(), name='show'),
    # Rutas del carrito de compras (usan sesiones para persistencia)
    path('cart/', CartView.as_view(), name='cart_index'),
    path('cart/add/<str:product_id>', CartView.as_view(), name='cart_add'),
    path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    # Rutas de imagen CON inversion de dependencias (DIP)
    # ImageLocalStorage() se inyecta desde aqui, la vista no la crea internamente
    path('image/', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_index'),
    path('image/save', ImageViewFactory(ImageLocalStorage()).as_view(), name='image_save'),
    # Rutas de imagen SIN inversion de dependencias (para comparacion)
    path('imagenotdi/', ImageViewNoDI.as_view(), name='imagenodi_index'),
    path('imagenotdi/save', ImageViewNoDI.as_view(), name='imagenodi_save'),
]