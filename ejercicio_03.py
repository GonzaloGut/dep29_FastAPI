from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(
    title="Tercera API",
    description="Esta es mi tercera API para practicar FastAPI con Pydantic",
    version="1.0.0",
)

class Item(BaseModel):
    codigo_producto: str
    descripcion: str
    precio: float
    cantidad: int

productos: List[Item] = []

@app.post("/items")
def crear_item(item: Item):
    productos.append(item)
    return item


@app.get("/items")
def leer_items():
    return productos
