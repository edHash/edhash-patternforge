from typing import Optional

from config import CantidadSolicitada
from parser_cantidad import ParserCantidad
from ui import UI


class SelectorCantidad:
    """
    Clase reutilizable para pedir cantidades.

    Puede usarse para:
    - combinaciones
    - patrones
    - líneas
    - registros
    """

    def __init__(self):
        self.parser = ParserCantidad()
        self.ui = UI()

    def mostrar_ayuda(self, nombre_unidad: str):
        self.ui.seccion("CANTIDAD DE SALIDA")

        print("Puedes indicar la cantidad de dos formas:")
        print(f"  100        = usar 100 {nombre_unidad}")
        print("  100mb      = usar aproximadamente 100 MB")
        print("  1gb        = usar aproximadamente 1 GB")
        print("  Enter      = usar TODO")

    def pedir(
        self,
        total: int,
        bytes_linea: int,
        nombre_unidad: str = "combinaciones",
        pregunta: Optional[str] = None
    ) -> Optional[CantidadSolicitada]:

        self.mostrar_ayuda(nombre_unidad)

        if pregunta is None:
            pregunta = f"\n¿Cuántas {nombre_unidad} deseas usar?: "

        entrada = input(
            self.ui.color(pregunta, "bold")
        ).strip()

        try:
            return self.parser.parsear(
                entrada=entrada,
                total=total,
                bytes_linea=bytes_linea
            )

        except ValueError as error:
            self.ui.error(str(error))
            return None