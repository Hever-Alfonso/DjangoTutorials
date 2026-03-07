# Proyecto Django - Comandos de referencia

Este documento describe los comandos necesarios para ejecutar y manejar el proyecto.

## Conceptos clave

- Imagen: plantilla construida a partir del Dockerfile.
- Contenedor: instancia en ejecucion de una imagen.
- Contenedores son efimeros: si se recrean, su sistema de archivos interno se pierde.
- Volumenes: almacenamiento persistente fuera del contenedor.
- En este proyecto, el volumen sqlite_data guarda la base de datos SQLite y el volumen media_data guarda las imagenes subidas por el usuario.

---

## Opcion 1: Correr con Conda (desarrollo local)

### Activar el entorno antes de cualquier comando
```bash
conda activate base
cd helloworld
```

### Comandos Django (solo con Conda activo)

Aplicar migraciones (crear o actualizar tablas en la base de datos):
```bash
python manage.py makemigrations
python manage.py migrate
```

Poblar la base de datos con 8 productos de prueba:
```bash
python manage.py seed_products
```

Abrir la consola interactiva de Django:
```bash
python manage.py shell
```

Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

Acceder en el navegador: http://127.0.0.1:8000

---

## Opcion 2: Correr con Docker (recomendado para entregar)

### IMPORTANTE: Docker tiene su propia base de datos separada
Cuando corres el proyecto con Docker por primera vez, la base de datos del contenedor
esta vacia. Debes aplicar migraciones y correr el seeder DENTRO del contenedor.
Esto se hace en una terminal separada mientras el contenedor esta corriendo.

### Paso 1: Levantar el contenedor

Desde la carpeta raiz del proyecto (donde esta docker-compose.yml):
```bash
docker compose up --build
```

Esperar hasta ver este mensaje en la terminal:
```
web-1 | Starting development server at http://0.0.0.0:8000/
```

### Paso 2: Aplicar migraciones (en una segunda terminal)

Abrir una segunda terminal en VS Code (icono + en el panel de terminal) y ejecutar:
```bash
docker compose exec web python helloworld/manage.py migrate
```

Resultado esperado: termina con "OK" en cada migracion aplicada.

### Paso 3: Poblar la base de datos con productos de prueba
```bash
docker compose exec web python helloworld/manage.py seed_products
```

Resultado esperado: "Successfully seeded products"

### Paso 4: Abrir en el navegador
```
http://localhost:8000
```

### Paso 5: Probar la API REST

Registrar usuario:
```bash
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testproducts", "password": "testpass123"}'
```

Login:
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testproducts", "password": "testpass123"}'
```

Listar productos (reemplaza <token> con el token retornado):
```bash
curl http://localhost:8000/api/products/ \
  -H "Authorization: Token <token>"
```

Crear producto:
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tv Samsung", "price": 1000}'
```

Actualizar producto:
```bash
curl -X PUT http://localhost:8000/api/products/1 \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tv Samsung 4K", "price": 1500}'
```

Borrar producto:
```bash
curl -X DELETE http://localhost:8000/api/products/1 \
  -H "Authorization: Token <token>"
```

### Otros comandos utiles con Docker

Correr cualquier comando de Django dentro del contenedor:
```bash
docker compose exec web python helloworld/manage.py <comando>
```

Ver los logs del contenedor en tiempo real:
```bash
docker compose logs -f
```

Detener el contenedor:
```bash
docker compose down
```

Detener el contenedor Y borrar los volumenes (reset total de BD e imagenes):
```bash
docker compose down -v
```

### Nota sobre persistencia con Docker

El volumen sqlite_data guarda la base de datos fuera del contenedor.
El volumen media_data guarda las imagenes subidas fuera del contenedor.
Esto significa que si bajas y vuelves a subir el contenedor con:
```bash
docker compose down
docker compose up --build
```
Los datos y las imagenes se conservan. Solo se pierden si usas docker compose down -v.