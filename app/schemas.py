# app/schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

# ==========================================
# --- ESQUEMAS PARA EL RECURSO LIBROS ---
# ==========================================
class LibroBase(BaseModel):
    id: int
    titulo: str
    autor: str
    disponible: Optional[bool] = True

class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    disponible: Optional[bool] = None

class LibroResponse(LibroBase):
    class Config:
        from_attributes = True


# ==========================================
# --- ESQUEMAS PARA EL RECURSO ESTUDIANTES ---
# ==========================================
class EstudianteBase(BaseModel):
    id: int
    nombre: str
    carrera: str

class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = None
    carrera: Optional[str] = None

class EstudianteResponse(EstudianteBase):
    class Config:
        from_attributes = True


# ==========================================
# --- ESQUEMAS PARA EL RECURSO PRÉSTAMOS ---
# ==========================================
class PrestamoCrear(BaseModel):
    libro_id: int
    estudiante_id: int

class PrestamoResponse(BaseModel):
    id: int
    libro_id: int
    estudiante_id: int
    fecha_prestamo: date
    devuelto: bool

    class Config:
        from_attributes = True