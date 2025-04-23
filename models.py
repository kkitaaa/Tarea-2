from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Crea una clase base para las definiciones de modelos
Base = declarative_base()

# Define el modelo Vuelo que representa la tabla "vuelos" en la base de datos
class Vuelo(Base):
    __tablename__ = "vuelos"  # Nombre de la tabla en la base de datos

    # Definición de columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)  # Columna de ID, clave primaria y con índice
    codigo = Column(String, unique=True, index=True)  # Columna para el código del vuelo, único y con índice
    destino = Column(String)  # Columna para el destino del vuelo
    emergencia = Column(Boolean, default=False)  # Columna para indicar si es una emergencia, por defecto False
