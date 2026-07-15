# main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import libros, estudiantes, prestamos

# Rutina para la inicialización y mapeo automático de tablas SQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Biblioteca Universitaria API",
    description="Manual Universitario de APIs Modulares con PostgreSQL Serverless.",
    version="2.1.0"
)

# Inyección de módulos independientes (Routers)
app.include_router(libros.router)
app.include_router(estudiantes.router)
app.include_router(prestamos.router)

@app.get("/")
def read_root():
    return {"status": "Online", "docs": "/docs"}