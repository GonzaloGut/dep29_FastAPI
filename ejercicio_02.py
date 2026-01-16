from fastapi import FastAPI

app = FastAPI(
    title="Mi API",
    description="Esta es mi API",
    version="1.0.0",
    contact={
        "name": "Bryan Vargas",
        "email": "bryan.vargas@example.com"
    }
)

lista_frutas = [
    {"item": "manzana", "stock": 5},
    {"item": "pera", "stock": 4},
    {"item": "mango", "stock": 3},
    {"item": "platano", "stock": 1},
    {"item": "cereza", "stock": 7},
]

@app.get("/")
def presentacion():
    return {"message": "Bienvenido a mi API"}

@app.get("/frutas")
def listar_frutas():
    return {"frutas": lista_frutas}

@app.get("/frutas/posicion")
def filtro_posicion_frutas(posicion: int):
    return {"fruta": lista_frutas[posicion]}

@app.get("/frutas/nombre")
def buscar_fruta_por_nombre(nombre: str):
    for fruta in lista_frutas:
        if fruta["item"] == nombre:
            return {"nombre de la fruta": nombre, "Stock de la fruta": fruta["stock"]}
    return {"message": "Fruta no encontrada"}