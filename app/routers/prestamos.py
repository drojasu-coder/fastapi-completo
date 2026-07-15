# app/routers/prestamos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import PrestamoModel, LibroModel, EstudianteModel
from app.schemas import PrestamoCrear, PrestamoResponse

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

# =====================================================================
# ENDPOINT: Generar Préstamo (Mutación de disponibilidad automática)
# =====================================================================
@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def generar_prestamo(prestamo: PrestamoCrear, db: Session = Depends(get_db)):
    # 1. Validación estricta de existencia del Estudiante
    estudiante = db.query(EstudianteModel).filter(EstudianteModel.id == prestamo.estudiante_id).first()
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Estudiante no registrado en la institución."
        )

    # 2. Validación de existencia física del Libro
    libro = db.query(LibroModel).filter(LibroModel.id == prestamo.libro_id).first()
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El libro seleccionado no existe en el catálogo."
        )

    # 3. Validación de inventario activo (Disponibilidad)
    if not libro.disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El ejemplar seleccionado no está disponible en este momento."
        )

    # 4. MUTACIÓN: Cambiar estado de disponibilidad del libro y crear registro del préstamo
    libro.disponible = False
    nuevo_prestamo = PrestamoModel(
        libro_id=prestamo.libro_id,
        estudiante_id=prestamo.estudiante_id
    )
    
    db.add(nuevo_prestamo)
    db.commit()
    db.refresh(nuevo_prestamo)
    return nuevo_prestamo


# =====================================================================
# ENDPOINT: Retornar Préstamo (Devolución y liberación de inventario)
# =====================================================================
@router.put("/{id}/devolver", response_model=PrestamoResponse)
def procesar_devolucion(id: int, db: Session = Depends(get_db)):
    # 1. Validación del registro de préstamo
    prestamo = db.query(PrestamoModel).filter(PrestamoModel.id == id).first()
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El identificador de préstamo no fue encontrado."
        )

    # 2. Validación preventiva si ya había sido entregado anteriormente
    if prestamo.devuelto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este préstamo ya se encuentra procesado y devuelto con anterioridad."
        )

    # 3. Recuperar libro asignado al préstamo para restaurar la disponibilidad
    libro = db.query(LibroModel).filter(LibroModel.id == prestamo.libro_id).first()
    if libro:
        libro.disponible = True  # El libro vuelve a estar libre

    # 4. MUTACIÓN: Marcar transacción de préstamo como completada
    prestamo.devuelto = True
    
    db.commit()
    db.refresh(prestamo)
    return prestamo


# =====================================================================
# ENDPOINT: Listado de todos los Préstamos
# =====================================================================
@router.get("/", response_model=List[PrestamoResponse])
def listar_prestamos(db: Session = Depends(get_db)):
    return db.query(PrestamoModel).all()


# =====================================================================
# ENDPOINT: Eliminación física de Préstamos (Acceso administrativo)
# =====================================================================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_registro_prestamo(id: int, db: Session = Depends(get_db)):
    prestamo = db.query(PrestamoModel).filter(PrestamoModel.id == id).first()
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Registro de préstamo no encontrado."
        )
    
    # Si el préstamo se va a eliminar y no fue devuelto, liberamos preventivamente el libro asociado
    if not prestamo.devuelto:
        libro = db.query(LibroModel).filter(LibroModel.id == prestamo.libro_id).first()
        if libro:
            libro.disponible = True

    db.delete(prestamo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)