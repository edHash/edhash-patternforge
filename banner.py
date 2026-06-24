from branding import (
    PROJECT_NAME,
    PROJECT_VERSION,
    PROJECT_AUTHOR,
    PROJECT_TAGLINE,
    PROJECT_DESCRIPTION
)


class BannerEdHash:
    """
    Banner visual de la herramienta.
    Mantiene separada la identidad visual del resto de la app.
    """

    def __init__(self, ui):
        self.ui = ui

    def mostrar(self):
        lineas = [
            "███████╗██████╗ ██╗  ██╗ █████╗ ███████╗██╗  ██╗",
            "██╔════╝██╔══██╗██║  ██║██╔══██╗██╔════╝██║  ██║",
            "█████╗  ██║  ██║███████║███████║███████╗███████║",
            "██╔══╝  ██║  ██║██╔══██║██╔══██║╚════██║██╔══██║",
            "███████╗██████╔╝██║  ██║██║  ██║███████║██║  ██║",
            "╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝",
        ]

        print()

        for linea in lineas:
            print(self.ui.color(linea.center(self.ui.ANCHO), "magenta"))

        print(
            self.ui.color(
                f">> {PROJECT_NAME} // {PROJECT_VERSION}".center(self.ui.ANCHO),
                "cyan"
            )
        )

        print(
            self.ui.color(
                f">> {PROJECT_TAGLINE}".center(self.ui.ANCHO),
                "gris"
            )
        )

        print(
            self.ui.color(
                f">> Crafted by {PROJECT_AUTHOR}".center(self.ui.ANCHO),
                "gris"
            )
        )

        print(
            self.ui.color(
                f">> {PROJECT_DESCRIPTION}".center(self.ui.ANCHO),
                "gris"
            )
        )

        print()