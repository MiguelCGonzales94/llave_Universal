# llave_Universal
Felicita - Backend API

📂 Arquitectura de Carpetas

Esta estructura sigue el patrón de diseño MVC (Model-View-Controller) adaptado a APIs modernas, separando responsabilidades para facilitar el mantenimiento y la escalabilidad.

felicita-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # 🚀 Punto de entrada (Entry Point)
│   ├── core/                   # Configuraciones del núcleo
│   │   ├── __init__.py
│   │   ├── config.py           # Variables de entorno y ajustes
│   │   └── database.py         # 🔌 Conexión a DB (Ya creado)
│   ├── models/                 # 🗄️ Modelos ORM (Tablas SQL)
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/                # 🛡️ Esquemas Pydantic (Validación de datos)
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── api/                    # 🌐 Endpoints (Rutas)
│       ├── __init__.py
│       └── routes.py           # Lógica de los endpoints
├── .env                        # 🔒 Variables de entorno (No subir a Git)
├── requirements.txt            # 📦 Dependencias
└── README.md


🛠️ Pasos para Levantar el Proyecto

Sigue estos pasos en tu terminal:

1. Crear entorno virtual

Es recomendable aislar las dependencias del proyecto.

# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate


2. Instalar dependencias

Instala las librerías definidas en requirements.txt.

pip install -r requirements.txt


3. Configurar Variables de Entorno

Crea un archivo llamado .env en la raíz del proyecto y agrega tu conexión a PostgreSQL (ajusta usuario y contraseña):

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/felicita
PROJECT_NAME="Felicita"
API_V1_STR="/api/v1"


4. Ejecutar el Servidor

Usa uvicorn para iniciar la aplicación en modo desarrollo (reload automático).

uvicorn app.main:app --reload


5. Verificar

Abre tu navegador en: http://127.0.0.1:8000/docs. Deberías ver la documentación automática (Swagger UI).