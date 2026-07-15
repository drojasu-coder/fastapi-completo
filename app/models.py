# app/models.py
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from datetime import date
from app.database import Base

class LibroModel(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    disponible = Column(Boolean, default=True)

class EstudianteModel(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    carrera = Column(String, nullable=False)

class PrestamoModel(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    fecha_prestamo = Column(Date, default=date.today)
    devuelto = Column(Boolean, default=False)