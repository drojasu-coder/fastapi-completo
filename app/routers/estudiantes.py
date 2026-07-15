# app/routers/estudiantes.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import EstudianteModel
from app.schemas import EstudianteBase, EstudianteUpdate, EstudianteResponse

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.post("/", response_model=EstudianteResponse, status_code=status.HTTP_201_CREATED)
def crear_estudiante(estudiante: EstudianteBase, db: Session = Depends(get_db)):
    db_est = db.query(EstudianteModel).filter(EstudianteModel.id == estudiante.id).first()
    if db_est:
        raise HTTPException(status_code=400, detail="El ID del estudiante ya existe.")
    nuevo_estudiante = EstudianteModel(**estudiante.model_dump())
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

@router.get("/", response_model=List[EstudianteResponse])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(EstudianteModel).all()

@router.get("/{id}", response_model=EstudianteResponse)
def obtener_estudiante(id: int, db: Session = Depends(get_db)):
    est = db.query(EstudianteModel).filter(EstudianteModel.id == id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return est

@router.put("/{id}", response_model=EstudianteResponse)
def actualizar_estudiante(id: int, estudiante_update: EstudianteUpdate, db: Session = Depends(get_db)):
    est = db.query(EstudianteModel).filter(EstudianteModel.id == id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    
    datos_actualizados = estudiante_update.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizados.items():
        setattr(est, clave, valor)
    
    db.commit()
    db.refresh(est)
    return est

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    est = db.query(EstudianteModel).filter(EstudianteModel.id == id).first()
    if not est:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    db.delete(est)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)