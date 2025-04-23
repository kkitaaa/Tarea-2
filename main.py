from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from models import Base, Vuelo  # Importa las definiciones de la base de datos y el modelo de Vuelo
from bd import engine, SessionLocal  # Importa el motor de la base de datos y la sesión local
from lista_vuelos import ListaDoblementeEnlazada  # Importa la estructura de lista doblemente enlazada
from undo_redo import registrar_accion, undo, redo  # Importa funciones para manejar acciones de deshacer/rehacer

# Inicializar FastAPI
app = FastAPI()

# Configuración de CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos usando el motor
Base.metadata.create_all(bind=engine)

# Instancia de la lista doblemente enlazada para manejar vuelos en memoria
lista_vuelos = ListaDoblementeEnlazada()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()  # Crea una nueva sesión
    try:
        yield db  # Proporciona la sesión para el uso del endpoint
    finally:
        db.close()  # Asegura que la sesión se cierre después de su uso

# -------------------------------
# ENDPOINTS CRUD
# -------------------------------

@app.post("/vuelos/")
def crear_vuelo(vuelo: dict, db: Session = Depends(get_db)):
    nuevo = Vuelo(**vuelo)  # Crea un nuevo objeto Vuelo a partir del diccionario recibido
    db.add(nuevo)  # Añade el nuevo vuelo a la sesión de base de datos
    db.commit()  # Confirma los cambios en la base de datos
    db.refresh(nuevo)  # Refresca el objeto para obtener el ID generado

    # Inserta el vuelo en la lista enlazada, al frente si es una emergencia
    if vuelo.get("emergencia"):
        lista_vuelos.insertar_al_frente(nuevo)
    else:
        lista_vuelos.insertar_al_final(nuevo)

    registrar_accion("add", nuevo)  # Registra la acción para permitir deshacer/rehacer
    return nuevo  # Devuelve el nuevo vuelo creado

@app.get("/vuelos/proximo/")
def obtener_proximo():
    vuelo = lista_vuelos.obtener_primero()  # Obtiene el primer vuelo de la lista
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos")  # Error si no hay vuelos
    return vuelo  # Devuelve el vuelo encontrado

@app.get("/vuelos/ultimo/")
def obtener_ultimo():
    vuelo = lista_vuelos.obtener_ultimo()  # Obtiene el último vuelo de la lista
    if not vuelo:
        raise HTTPException(status_code=404, detail="No hay vuelos")  # Error si no hay vuelos
    return vuelo  # Devuelve el vuelo encontrado

@app.get("/vuelos/longitud/")
def obtener_longitud():
    return {"total": lista_vuelos.longitud()}  # Devuelve la longitud de la lista de vuelos

@app.delete("/vuelos/{posicion}")
def eliminar_por_posicion(posicion: int):
    vuelo = lista_vuelos.extraer_de_posicion(posicion)  # Extrae el vuelo en la posición dada
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")  # Error si el vuelo no existe

    registrar_accion("remove", vuelo)  # Registra la acción para permitir deshacer/rehacer
    return vuelo  # Devuelve el vuelo eliminado

# UNDO / REDO
@app.post("/undo/")
def deshacer():
    return {"resultado": undo(lista_vuelos)}  # Llama a la función de deshacer y devuelve el resultado

@app.post("/redo/")
def rehacer():
    return {"resultado": redo(lista_vuelos)}  # Llama a la función de rehacer y devuelve el resultado

# para correr el servidor
# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
