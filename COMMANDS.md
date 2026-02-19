# Proyecto Django - Comandos de referencia

Este documento describe los comandos necesarios para ejecutar y manejar el proyecto.

## Conceptos clave

- Imagen: plantilla construida a partir del Dockerfile.
- Contenedor: instancia en ejecucion de una imagen.
- Contenedores son efimeros: si se recrean, su sistema de archivos interno se pierde.
- Volumenes: almacenamiento persistente fuera del contenedor.
- En este proyecto, el volumen guarda la base de datos SQLite.

## Entorno Conda

Activar el entorno del proyecto antes de ejecutar cualquier comando:
```bash
conda activate hever_tutorial_2
```

## Comandos Django

Aplicar migraciones (crear o actualizar tablas en la base de datos):
```bash
python manage.py makemigrations
python manage.py migrate
```

Poblar la base de datos con productos de prueba (8 productos aleatorios):
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

## Levantar el proyecto con Docker
```bash
docker compose up --build
```

Una vez el contenedor este corriendo, acceder en el navegador:

http://localhost:8000