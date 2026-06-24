from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ConfiguracionDiccionario:
    caracteres: str
    longitud: int
    carpeta: str
    total_combinaciones: int
    bytes_por_linea: int
    espacio_libre: int
    maximo_recomendado: int


@dataclass(frozen=True)
class CantidadSolicitada:
    cantidad: int
    modo: str
    bytes_solicitados: Optional[int] = None


@dataclass(frozen=True)
class SeleccionGeneracion:
    cantidad: int
    modo: str
    tamano_estimado: int
    bytes_solicitados: Optional[int] = None

@dataclass(frozen=True)
class ResultadoArchivo:
    ruta_archivo: str
    elementos_escritos: int
    tiempo_segundos: float
    tamano_real: int
    nombre_elemento: str