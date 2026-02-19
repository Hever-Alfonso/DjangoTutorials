# Tutorial 2 - Arquitectura de Software (Django)

Proyecto desarrollado como parte del Taller 2 de Arquitectura de Software, utilizando el framework Django con persistencia real en base de datos, modelos, migraciones, factories y relaciones entre modelos.

El proyecto fue construido de manera incremental sobre el Tutorial 1, siguiendo estrictamente las actividades definidas en el documento guia del taller y manteniendo buenas practicas de desarrollo y control de versiones con Git.

---

## Descripcion del proyecto

La aplicacion representa una tienda en linea que ahora persiste datos realmente en una base de datos SQLite. El objetivo principal es comprender:

- La creacion y uso de modelos Django
- El sistema de migraciones
- El uso de factories y seeders para datos de prueba
- Las relaciones entre modelos (ForeignKey)
- El ORM de Django para consultar la base de datos
- El flujo completo de una aplicacion web con persistencia real

---

## Arquitectura aplicada (MVT)

El proyecto sigue el patron MVT (Model - View - Template) de Django:

### Model
- Modelo `Product` con campos: name, price, created_at, updated_at
- Modelo `Comment` relacionado con Product mediante ForeignKey
- Migraciones generadas automaticamente por Django

### View
- Consultas reales a la base de datos mediante el ORM de Django
- Formularios basados en ModelForm para guardar directamente en la BD
- Vistas genericas de Django (ListView)

### Template
- Listado de productos desde la base de datos
- Detalle de producto con comentarios relacionados
- Formulario de creacion con confirmacion

---

## Tecnologias utilizadas

- Python 3.12
- Django 5.2
- factory-boy y Faker (generacion de datos de prueba)
- HTML (Django Templates)
- CSS
- Bootstrap
- SQLite
- Git y GitHub
- Conda (entorno virtual)

---

## Estructura del proyecto
```
.
├── helloworld/
│   ├── helloworld_project/
│   ├── pages/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_products.py
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   │   ├── pages/
│   │   │   └── products/
│   │   ├── factories.py
│   │   ├── models.py
│   │   ├── urls.py
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

- Listado de productos desde la base de datos
- Detalle de producto con precio condicional (rojo si supera 2000)
- Comentarios relacionados al producto
- Creacion de productos mediante formulario con persistencia en BD
- Confirmacion de creacion
- Seeder para poblar la BD con datos de prueba
- Migraciones de base de datos

---

## Como ejecutar el proyecto

### Opcion 1: Conda

1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd DjangoTutorials
```

2. Crear y activar el entorno
```bash
conda create -n hever_tutorial_2 python=3.12
conda activate hever_tutorial_2
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

Acceder en: http://localhost:8000

---

## Control de versiones

El proyecto utiliza Git siguiendo buenas practicas:

- Desarrollo en rama `feat/tutorial-02-django-models`
- Commits con convencion Conventional Commits
- Historial limpio y trazable

Ejemplo de commit:
```
feat(pages): add Product model with migration
```

---

## Autor

Hever Andre Alfonso Jimenez - Universidad EAFIT - Proyecto desarrollado como parte de un taller academico de Arquitectura de Software utilizando Django.