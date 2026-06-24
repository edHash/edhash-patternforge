import time

from utilidades import Formateador


class BarraProgreso:
    """
    Clase reutilizable para mostrar progreso en terminal.

    Sirve para:
    - Generación normal de combinaciones
    - Auditoría por área
    - Cualquier proceso futuro que tenga total y avance
    """

    def __init__(self, total: int, ancho: int = 30):
        self.total = total
        self.ancho = ancho
        self.inicio = time.time()

    @staticmethod
    def calcular_intervalo(total: int) -> int:
        """
        Calcula cada cuántas iteraciones actualizar la barra.
        Evita imprimir demasiado y hacer lento el programa.
        """

        return max(
            1,
            min(100000, total // 1000)
        )

    def tiempo_transcurrido(self) -> float:
        return time.time() - self.inicio

    def mostrar(self, actual: int):
        if self.total <= 0:
            porcentaje = 1
        else:
            porcentaje = actual / self.total

        porcentaje = min(max(porcentaje, 0), 1)

        llenado = int(self.ancho * porcentaje)

        barra = "#" * llenado + "-" * (self.ancho - llenado)

        transcurrido = self.tiempo_transcurrido()

        if transcurrido > 0:
            velocidad = actual / transcurrido
        else:
            velocidad = 0

        restante = self.total - actual

        if velocidad > 0:
            tiempo_restante = restante / velocidad
        else:
            tiempo_restante = 0

        print(
            f"\r[{barra}] "
            f"{porcentaje * 100:6.2f}% | "
            f"{actual:,}/{self.total:,} | "
            f"{velocidad:,.0f}/s | "
            f"ETA: {Formateador.tiempo_legible(tiempo_restante)}",
            end="",
            flush=True
        )