# Tutorial 4 - Arquitectura de Software (Django)

Proyecto desarrollado como parte del Taller 4 de Arquitectura de Software, extendiendo el Tutorial 3 con una API REST construida con Django REST Framework (DRF) para el modelo Product, manteniendo las vistas MVT existentes sin modificaciones.

El proyecto fue construido de manera incremental sobre el Tutorial 3, siguiendo estrictamente las actividades definidas en el documento guia del taller y manteniendo buenas practicas de desarrollo y control de versiones con Git.

---

## Descripcion del proyecto

La aplicacion representa una tienda en linea que expone dos interfaces en paralelo:

- **MVT (Tutorial 3)**: vistas HTML con templates Django para el navegador
- **REST API (Tutorial 4)**: endpoints JSON con autenticacion por token para clientes externos

El objetivo principal del Tutorial 4 es comprender:

- Como construir una API REST con Django REST Framework
- Serializers para convertir modelos a JSON
- Vistas genericas de DRF: ListCreateAPIView, RetrieveUpdateDestroyAPIView
- Autenticacion por token con rest_framework.authtoken
- Endpoints de signup y login
- Coexistencia de MVT y REST API en el mismo proyecto Django

---

## Arquitectura aplicada (MVT + REST API)

El proyecto sigue el patron MVT de Django e incorpora una capa de API REST:

### Model
- Modelo `Product` con campos: name, price, created_at, updated_at
- Modelo `Comment` relacionado con Product mediante ForeignKey
- Migraciones generadas automaticamente por Django

### View (MVT - Tutorial 3)
- Consultas reales a la base de datos mediante el ORM de Django
- Formularios basados en ModelForm para guardar directamente en la BD
- `CartView`: usa `request.session` para almacenar el carrito entre peticiones
- `CartRemoveAllView`: elimina el carrito de la sesion actual
- `ImageViewFactory`: factory function que inyecta el storage como dependencia (DIP)
- `ImageViewNoDI`: misma funcionalidad pero con acoplamiento directo (sin DIP)

### REST API (Tutorial 4)
- `ProductSerializer`: convierte instancias de Product a JSON
- `ProductListCreate`: GET y POST en /api/products/
- `ProductRetrieveUpdateDestroy`: GET, PUT y DELETE en /api/products/<pk>
- `signup`: POST /api/signup/ — registra usuario y retorna token
- `login`: POST /api/login/ — autentica usuario y retorna token
- Autenticacion por token en todos los endpoints de la API

### Template
- Listado de productos desde la base de datos
- Detalle de producto con comentarios relacionados
- Formulario de creacion con confirmacion
- Pagina de carrito de compras
- Pagina de subida de imagenes (con y sin DI)

### DIP - Inversion de Dependencias
- `interfaces.py`: define `ImageStorage` como clase abstracta (el contrato)
- `utils.py`: implementa `ImageLocalStorage` que hereda de `ImageStorage`
- `apps.py`: service provider que carga la clase configurada al arrancar
- `settings.py`: `IMAGE_STORAGE_CLASS` permite cambiar la implementacion sin tocar vistas
- `urls.py`: inyecta `ImageLocalStorage()` al crear las vistas (inyeccion de dependencias)

---

## Endpoints de la API REST

| Metodo | URL | Auth | Descripcion |
|--------|-----|------|-------------|
| POST | /api/signup/ | No | Registrar usuario, retorna token |
| POST | /api/login/ | No | Autenticar usuario, retorna token |
| GET | /api/products/ | Token | Listar todos los productos |
| POST | /api/products/ | Token | Crear nuevo producto |
| GET | /api/products/<pk> | Token | Detalle de un producto |
| PUT | /api/products/<pk> | Token | Actualizar un producto |
| DELETE | /api/products/<pk> | Token | Eliminar un producto |

El token se envia en el header de cada peticion autenticada:
```
Authorization: Token <tu_token>
```

---

## Tecnologias utilizadas

- Python 3.12
- Django 5.2
- Django REST Framework 3.16.1
- factory-boy y Faker (generacion de datos de prueba)
- HTML (Django Templates)
- CSS
- Bootstrap
- SQLite
- Git y GitHub
- Conda (entorno virtual)
- Docker y Docker Compose

---

## Estructura del proyecto
```
.
├── helloworld/
│   ├── helloworld_project/
│   ├── media/                    # Imagenes subidas (persistidas con volumen Docker)
│   ├── api/                      # App REST API (Tutorial 4)
│   │   ├── serializers.py        # ProductSerializer
│   │   ├── views.py              # Vistas genericas DRF + signup + login
│   │   └── urls.py               # Rutas bajo /api/
│   ├── pages/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_products.py
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   │   ├── cart/
│   │   │   │   └── index.html
│   │   │   ├── images/
│   │   │   │   └── index.html
│   │   │   ├── imagesnotdi/
│   │   │   │   └── index.html
│   │   │   ├── pages/
│   │   │   └── products/
│   │   ├── factories.py
│   │   ├── interfaces.py         # Interfaz abstracta ImageStorage (DIP)
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── utils.py              # Implementacion concreta ImageLocalStorage
│   │   └── views.py
│   └── manage.py
├── .gitignore
├── COMMANDS.md
├── Dockerfile
├── README.md
├── docker-compose.yml
└── requirements.txt
```

---

## Funcionalidades implementadas

### Tutorial 3 (MVT)
- Listado de productos desde la base de datos
- Detalle de producto con precio condicional (rojo si supera 2000)
- Comentarios relacionados al producto
- Creacion de productos mediante formulario con persistencia en BD
- Seeder para poblar la BD con datos de prueba
- Carrito de compras con sesiones Django (agregar y vaciar productos)
- Subida de imagenes con Inversion de Dependencias (DIP)
- Subida de imagenes sin DI (para comparacion y entendimiento del principio)

### Tutorial 4 (REST API)
- Signup y login con autenticacion por token
- CRUD completo de productos via API REST
- Proteccion de endpoints con IsAuthenticated

---

## Como ejecutar el proyecto

### Opcion 1: Conda

1. Clonar el repositorio
```bash
git clone https://github.com/Hever-Alfonso/DjangoTutorials.git
cd DjangoTutorials
```

2. Activar el entorno
```bash
conda activate base
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones y poblar la base de datos
```bash
cd helloworld
python manage.py migrate
python manage.py seed_products
```

5. Ejecutar el servidor
```bash
python manage.py runserver
```

6. Abrir en el navegador
```
http://127.0.0.1:8000/
```

### Opcion 2: Docker
```bash
docker compose up --build
```

En una segunda terminal:
```bash
docker compose exec web python helloworld/manage.py migrate
docker compose exec web python helloworld/manage.py seed_products
```

Acceder en: http://localhost:8000

---

## Control de versiones

El proyecto utiliza Git siguiendo buenas practicas:

- Desarrollo en ramas `feat/` por actividad
- Commits con convencion Conventional Commits
- Historial limpio y trazable

Ejemplo de commit:
```
feat(api): add serializers, views and urls for Product REST API
```

---

## Autor

Hever Andre Alfonso Jimenez - Universidad EAFIT - Proyecto desarrollado como parte de un taller academico de Arquitectura de Software utilizando Django.