from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from pages.models import Product
from .serializers import ProductSerializer


class ProductListCreate(generics.ListCreateAPIView):
    # ListCreateAPIView maneja dos metodos HTTP en una sola clase:
    # GET  /api/products/ -> lista todos los productos
    # POST /api/products/ -> crea un nuevo producto
    serializer_class = ProductSerializer

    # IsAuthenticated: el cliente DEBE enviar un token valido en el header:
    # Authorization: Token <token>
    # Si no lo envia, retorna 401 Unauthorized automaticamente.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna todos los productos ordenados por fecha de creacion descendente
        # (el mas reciente primero)
        return Product.objects.all().order_by('-created_at')


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    # RetrieveUpdateDestroyAPIView maneja tres metodos HTTP:
    # GET    /api/products/<pk> -> detalle de un producto
    # PUT    /api/products/<pk> -> actualiza un producto
    # DELETE /api/products/<pk> -> borra un producto
    # <pk> es el ID numerico del producto capturado desde la URL
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    # A diferencia de ToDoRetrieveUpdateDestroy en el todoapp, aqui
    # cualquier usuario autenticado puede ver/editar/borrar cualquier
    # producto, porque Product no tiene ForeignKey a User.
    queryset = Product.objects.all()


@csrf_exempt
# csrf_exempt: deshabilita la proteccion CSRF para este endpoint.
# Es necesario porque los clientes API no tienen cookies de sesion.
def signup(request):
    # POST /api/signup/ con body: {"username": "x", "password": "y"}
    # Retorna: {"token": "<token_generado>"}
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            # Crea el usuario en la tabla auth_user de Django
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'])
            user.save()
            # Crea el token en la tabla authtoken_token
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            # Se lanza si el username ya existe en la base de datos
            return JsonResponse(
                {'error': 'username taken. choose another username'},
                status=400)


@csrf_exempt
def login(request):
    # POST /api/login/ con body: {"username": "x", "password": "y"}
    # Retorna: {"token": "<token_del_usuario>"}
    if request.method == 'POST':
        data = JSONParser().parse(request)
        # authenticate() verifica username y password contra la BD.
        # Retorna el objeto User si es valido, None si no lo es.
        user = authenticate(request,
                            username=data['username'],
                            password=data['password'])
        if user is None:
            return JsonResponse(
                {'error': 'unable to login. check username and password'},
                status=400)
        else:
            try:
                # Busca el token existente del usuario
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                # Si no tiene token (ej. creado via admin), crea uno nuevo
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)