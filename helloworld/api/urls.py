from django.urls import path
from . import views

urlpatterns = [
    # GET  /api/products/    -> lista todos los productos
    # POST /api/products/    -> crea un nuevo producto
    path('products/', views.ProductListCreate.as_view(), name='product_list'),

    # GET    /api/products/<pk> -> detalle de un producto
    # PUT    /api/products/<pk> -> actualiza un producto
    # DELETE /api/products/<pk> -> borra un producto
    # <int:pk> captura el ID numerico de la URL y lo pasa a la vista
    path('products/<int:pk>', views.ProductRetrieveUpdateDestroy.as_view(), name='product_RUD'),

    # POST /api/signup/ -> registrar usuario nuevo, retorna token
    path('signup/', views.signup, name='signup'),

    # POST /api/login/ -> autenticar usuario existente, retorna token
    path('login/', views.login, name='login'),
]