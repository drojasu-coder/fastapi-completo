# app/database.py
# Importa create_engine, que permite crear la conexión con la base de datos.
from sqlalchemy import create_engine
# declarative_base() sirve para crear la clase base de la que heredarán
# todos nuestros modelos (tablas).
# sessionmaker() crea un objeto encargado de generar sesiones de trabajo
# con la base de datos.
from sqlalchemy.orm import declarative_base, sessionmaker
# Importa la configuración del proyecto (variables de entorno)
# como la cadena de conexión a la base de datos.
from app.config import settings
# Obtiene la URL de conexión definida en el archivo .env
db_url = settings.DATABASE_URL
# ------------------------------------------------------------
# Compatibilidad con PostgreSQL
# ------------------------------------------------------------
# Algunas plataformas (como versiones antiguas de Heroku o Render)
# utilizan el prefijo "postgres://".
# SQLAlchemy 1.4+ y 2.x requieren que el protocolo sea
# "postgresql://". Si encontramos el formato antiguo,
# lo reemplazamos automáticamente para evitar errores.
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
# ------------------------------------------------------------
# Crear el motor de conexión (Engine)
# ------------------------------------------------------------
# El Engine administra las conexiones físicas con la base de datos.
# Todas las consultas realizadas por SQLAlchemy pasarán por este objeto.
engine = create_engine(db_url)
# ------------------------------------------------------------
# Crear el generador de sesiones
# ------------------------------------------------------------
# Una sesión representa una conversación entre la aplicación
# y la base de datos.
#
# autocommit=False
#   Los cambios NO se guardan automáticamente.
#   Debemos ejecutar db.commit() para confirmar la transacción.
#
# autoflush=False
#   Evita que SQLAlchemy envíe automáticamente cambios pendientes
#   antes de ejecutar una consulta.
#
# bind=engine
#   Indica qué motor de conexión utilizará la sesión.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
# ------------------------------------------------------------
# Clase base para todos los modelos
# ------------------------------------------------------------
# Cada tabla del proyecto heredará de Base.
# Ejemplo:
# class Usuario(Base):
#     __tablename__ = "usuarios"
Base = declarative_base()
# ------------------------------------------------------------
# Dependencia de FastAPI para obtener una sesión de base de datos
# ------------------------------------------------------------
def get_db():
    """
    Crea una sesión de conexión a la base de datos.
    Esta función se utiliza como dependencia en FastAPI mediante
    Depends(get_db).
    El uso de 'yield' permite entregar la sesión al endpoint y,
    cuando la petición termina (con éxito o con error), ejecutar
    automáticamente el bloque 'finally' para liberar los recursos.
    Esto evita fugas de memoria y conexiones abiertas innecesariamente.
    """
    # Crear una nueva sesión
    db = SessionLocal()
    try:
        # Entregar la sesión al endpoint
        yield db
    finally:
        # Cerrar siempre la conexión al finalizar la petición
        db.close()