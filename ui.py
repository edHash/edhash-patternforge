import os
from typing import Iterable, Optional, Sequence, Tuple


class UI:
    """
    Capa visual para mejorar la experiencia de usuario en terminal.
    Centraliza títulos, menús, mensajes, confirmaciones e inputs.
    """

    ANCHO = 70

    COLORES = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "dim": "\033[2m",
        "rojo": "\033[91m",
        "verde": "\033[92m",
        "amarillo": "\033[93m",
        "azul": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "gris": "\033[90m",
    }

    def __init__(self, usar_color: bool = True):
        if os.name == "nt":
            os.system("")

        self.usar_color = (
            usar_color
            and os.getenv("NO_COLOR") is None
        )

    def color(self, texto: str, color: str) -> str:
        if not self.usar_color:
            return texto

        codigo = self.COLORES.get(color, "")
        reset = self.COLORES["reset"]

        return f"{codigo}{texto}{reset}"

    def limpiar(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pausa(self):
        input(
            self.color(
                "\nPresiona Enter para volver al menú...",
                "gris"
            )
        )

    def linea(self, caracter: str = "="):
        print(caracter * self.ANCHO)

    def titulo(self, texto: str, subtitulo: Optional[str] = None):
        self.linea("=")
        print(self.color(texto.center(self.ANCHO), "cyan"))
        self.linea("=")

        if subtitulo:
            print(self.color(subtitulo, "gris"))

    def seccion(self, texto: str):
        print("\n" + "=" * self.ANCHO)
        print(self.color(texto, "bold"))
        print("=" * self.ANCHO)

    def info(self, mensaje: str):
        print(self.color(f"[INFO] {mensaje}", "cyan"))

    def exito(self, mensaje: str):
        print(self.color(f"[OK] {mensaje}", "verde"))

    def advertencia(self, mensaje: str):
        print(self.color(f"[ADVERTENCIA] {mensaje}", "amarillo"))

    def error(self, mensaje: str):
        print(self.color(f"[ERROR] {mensaje}", "rojo"))

    def campo(self, nombre: str, valor):
        print(f"{nombre:<28}: {valor}")

    def resumen(
        self,
        titulo: str,
        campos: Sequence[Tuple[str, object]]
    ):
        self.seccion(titulo)

        for nombre, valor in campos:
            self.campo(nombre, valor)

    def menu(
        self,
        titulo: str,
        opciones: Sequence[Tuple[str, str]],
        subtitulo: Optional[str] = None
    ):
        self.limpiar()
        self.titulo(titulo, subtitulo)

        for numero, descripcion in opciones:
            numero_formateado = self.color(f"{numero}.", "cyan")
            print(f"{numero_formateado} {descripcion}")

        self.linea("=")

    def pedir_opcion(self, opciones_validas: Iterable[str]) -> str:
        opciones_validas = set(opciones_validas)

        while True:
            opcion = input(
                self.color("\nElige una opción: ", "bold")
            ).strip()

            if opcion in opciones_validas:
                return opcion

            self.error("Opción inválida. Intenta de nuevo.")

    def confirmar(
        self,
        pregunta: str,
        defecto: Optional[bool] = None
    ) -> bool:
        if defecto is True:
            sufijo = " [S/n]: "
        elif defecto is False:
            sufijo = " [s/N]: "
        else:
            sufijo = " [s/n]: "

        while True:
            respuesta = input(
                self.color(pregunta + sufijo, "bold")
            ).strip().lower()

            if respuesta == "" and defecto is not None:
                return defecto

            if respuesta in ("s", "si", "sí"):
                return True

            if respuesta in ("n", "no"):
                return False

            self.error("Respuesta inválida. Escribe s o n.")

    def entrada(
        self,
        pregunta: str,
        requerido: bool = False,
        defecto: Optional[str] = None
    ) -> str:
        while True:
            if defecto is not None:
                texto_pregunta = f"{pregunta} [{defecto}]: "
            else:
                texto_pregunta = f"{pregunta}: "

            respuesta = input(
                self.color(texto_pregunta, "bold")
            ).strip()

            if respuesta == "" and defecto is not None:
                return defecto

            if respuesta == "" and requerido:
                self.error("Este campo es obligatorio.")
                continue

            return respuesta