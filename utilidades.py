import os
import math


class UtilidadesSistema:

    @staticmethod
    def limpiar_pantalla():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pausar():
        input("\nPresiona Enter para volver al menú...")

    @staticmethod
    def normalizar_carpeta(carpeta: str) -> str:
        if carpeta.strip() == "":
            carpeta = os.getcwd()

        return os.path.abspath(os.path.expanduser(carpeta))

    @staticmethod
    def carpeta_valida(carpeta: str) -> bool:
        return os.path.exists(carpeta) and os.path.isdir(carpeta)


class Formateador:

    @staticmethod
    def tamano_legible(bytes_: int) -> str:
        unidades = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]

        tamano = float(bytes_)
        indice = 0

        while tamano >= 1024 and indice < len(unidades) - 1:
            tamano /= 1024
            indice += 1

        return f"{tamano:.2f} {unidades[indice]}"

    @staticmethod
    def tiempo_legible(segundos: float) -> str:
        segundos = int(segundos)

        if segundos < 60:
            return f"{segundos} s"

        minutos, segundos = divmod(segundos, 60)

        if minutos < 60:
            return f"{minutos} min {segundos} s"

        horas, minutos = divmod(minutos, 60)

        if horas < 24:
            return f"{horas} h {minutos} min"

        dias, horas = divmod(horas, 24)
        return f"{dias} d {horas} h"


class CalculadoraTamano:

    @staticmethod
    def bytes_por_linea(caracteres: str, longitud: int) -> int:
        promedio_bytes_caracter = sum(
            len(c.encode("utf-8")) for c in caracteres
        ) / len(caracteres)

        return math.ceil((promedio_bytes_caracter * longitud) + 1)

    @staticmethod
    def estimar_tamano(bytes_linea: int, cantidad: int) -> int:
        return bytes_linea * cantidad