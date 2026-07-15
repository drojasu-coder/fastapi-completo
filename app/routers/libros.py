# app/routers/libros.py
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import LibroModel
from app.schemas import LibroBase, LibroUpdate, LibroResponse

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=LibroResponse, status_code=status.HTTP_201_CREATED)
def crear_libro(libro: LibroBase, db: Session = Depends(get_db)):
    db_libro = db.query(LibroModel).filter(LibroModel.id == libro.id).first()
    if db_libro:
        raise HTTPException(status_code=400, detail="El ID del libro ya existe.")
    nuevo_libro = LibroModel(**libro.model_dump())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

@router.get("/", response_model=List[LibroResponse])
def listar_libros(db: Session = Depends(get_db)):
    return db.query(LibroModel).all()

@router.get("/{id}", response_model=LibroResponse)
def obtener_libro(id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).filter(LibroModel.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    return libro

@router.put("/{id}", response_model=LibroResponse)
def actualizar_libro(id: int, libro_update: LibroUpdate, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).filter(LibroModel.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    
    # Actualizar solo los atributos enviados por el cliente
    datos_actualizados = libro_update.model_dump(exclude_unset=True)
    for clave, valor in datos_actualizados.items():
        setattr(libro, clave, valor)
    
    db.commit()
    db.refresh(libro)
    return libro

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).filter(LibroModel.id == id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    db.delete(libro)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)