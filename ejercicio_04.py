import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List


app = FastAPI(
    title="Cuarta API",
    description="Esta es mi cuarta API para practicar FastAPI con SQLite",
    version="1.0.0",
)

DATABASE_NAME = "estudiantes.db"

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                carrera TEXT NOT NULL,
                semestre INTEGER NOT NULL,
                activo BOOLEAN DEFAULT 1,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()

class EstudianteBase(BaseModel):
    nombre: str
    email: EmailStr
    carrera: str
    semestre: int

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    carrera: Optional[str] = None
    semestre: Optional[int] = None
    activo: Optional[bool] = None


class EstudianteResponse(EstudianteBase):
    id: int
    activo: bool
    fecha_registro: str

    class Config:
        from_attributes = True


@app.post("/estudiantes/", response_model=EstudianteResponse)
def crear_estudiante(estudiante: EstudianteCreate):
    with get_db_connection() as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO estudiantes (nombre, email, carrera, semestre)
                VALUES (?, ?, ?, ?)
                """,
                (estudiante.nombre, estudiante.email, estudiante.carrera, estudiante.semestre)
            )
            conn.commit()
            
            nuevo_estudiante = conn.execute(
                "SELECT * FROM estudiantes WHERE id = ?",
                (cursor.lastrowid,)
            ).fetchone()
            
            return dict(nuevo_estudiante)
            
        except sqlite3.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {estudiante.email} ya está registrado"
            )


@app.get("/estudiantes/", response_model=List[EstudianteResponse])
def listar_estudiantes(
    skip: int = 0,
    limit: int = 100,
    solo_activos: bool = True
):
    with get_db_connection() as conn:
        if solo_activos:
            query = "SELECT * FROM estudiantes WHERE activo = 1 LIMIT ? OFFSET ?"
        else:
            query = "SELECT * FROM estudiantes LIMIT ? OFFSET ?"
        
        estudiantes = conn.execute(query, (limit, skip)).fetchall()
        return [dict(e) for e in estudiantes]


@app.get("/estudiantes/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(estudiante_id: int):
    with get_db_connection() as conn:
        estudiante = conn.execute(
            "SELECT * FROM estudiantes WHERE id = ?",
            (estudiante_id,)
        ).fetchone()
        
        if estudiante is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado"
            )
        
        return dict(estudiante)
