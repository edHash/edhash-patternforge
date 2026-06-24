import os

from auditoria import ModuloAuditoriaArea
from analizador import AnalizadorDiccionario
from generador import GeneradorCombinaciones
from selector_cantidad import SelectorCantidad
from utilidades import UtilidadesSistema, Formateador
from reporte import ReporteGeneracion
from ui import UI
from banner import BannerEdHash
from branding import PROJECT_NAME, PROJECT_SHORT_NAME, PROJECT_DESCRIPTION


class MenuApp:

    def __init__(self):
        self.ui = UI()
        self.banner = BannerEdHash(self.ui)
        self.analizador = AnalizadorDiccionario()
        self.generador = GeneradorCombinaciones()
        self.selector_cantidad = SelectorCantidad()
        self.auditoria = ModuloAuditoriaArea()
        self.reporte = ReporteGeneracion()

    def iniciar(self):
        while True:
            self.mostrar_menu()

            opcion = self.ui.pedir_opcion(
                opciones_validas={"1", "2", "3", "4", "5"}
            )

            if opcion == "1":
                self.opcion_generar_combinaciones()

            elif opcion == "2":
                self.opcion_solo_calcular()

            elif opcion == "3":
                self.mostrar_ejemplos()

            elif opcion == "4":
                self.auditoria.ejecutar()

            elif opcion == "5":
                self.ui.exito("Saliendo del programa...")
                break

    def mostrar_menu(self):
        self.ui.limpiar()
        self.banner.mostrar()

        self.ui.titulo(
            PROJECT_NAME.upper(),
            PROJECT_DESCRIPTION
        )

        print(self.ui.color("1.", "cyan"), "Forjar diccionario en archivo .txt")
        print(self.ui.color("2.", "cyan"), "Simular peso y combinaciones")
        print(self.ui.color("3.", "cyan"), "Ver ejemplos de uso")
        print(self.ui.color("4.", "cyan"), "Modo auditoría por área")
        print(self.ui.color("5.", "cyan"), "Salir")

        self.ui.linea("=")

    def pedir_caracteres_y_longitud(self):
        caracteres = input("\nIngresa los caracteres a utilizar: ")

        caracteres = "".join(dict.fromkeys(caracteres))

        if not caracteres:
            print("❌ Debes ingresar al menos un carácter.")
            return None, None

        try:
            longitud = int(input("Longitud de las combinaciones: "))

            if longitud <= 0:
                print("❌ La longitud debe ser mayor que cero.")
                return None, None

        except ValueError:
            print("❌ Longitud inválida.")
            return None, None

        return caracteres, longitud

    def pedir_carpeta(self):
        carpeta = input(
            "\nCarpeta donde guardar o analizar "
            "(Enter = carpeta actual): "
        ).strip()

        carpeta = UtilidadesSistema.normalizar_carpeta(carpeta)

        if not UtilidadesSistema.carpeta_valida(carpeta):
            print("❌ La carpeta indicada no existe o no es válida.")
            return None

        return carpeta

    def crear_configuracion_desde_usuario(self):
        caracteres, longitud = self.pedir_caracteres_y_longitud()

        if caracteres is None:
            return None

        carpeta = self.pedir_carpeta()

        if carpeta is None:
            return None

        return self.analizador.crear_configuracion(
            caracteres=caracteres,
            longitud=longitud,
            carpeta=carpeta
        )

    def pedir_seleccion(self, config):
        solicitud = self.selector_cantidad.pedir(
            total=config.total_combinaciones,
            bytes_linea=config.bytes_por_linea,
            nombre_unidad="combinaciones"
        )

        if solicitud is None:
            return None

        return self.analizador.crear_seleccion(
            solicitud=solicitud,
            config=config
        )

    def pedir_ruta_archivo(self, carpeta):
        nombre = input("\nNombre del archivo sin .txt: ").strip()

        if nombre == "":
            nombre = "combinaciones"

        nombre += ".txt"

        ruta = os.path.join(carpeta, nombre)

        if os.path.exists(ruta):
            sobrescribir = input(
                "\n⚠️ El archivo ya existe. "
                "¿Deseas sobrescribirlo? (s/n): "
            ).lower()

            if sobrescribir != "s":
                print("Operación cancelada.")
                return None

        return ruta

    def opcion_generar_combinaciones(self):
        self.ui.limpiar()
        self.ui.titulo(
            "GENERAR COMBINACIONES",
            "Crea un archivo .txt usando caracteres personalizados."
        )

        config = self.crear_configuracion_desde_usuario()

        if config is None:
            UtilidadesSistema.pausar()
            return

        self.analizador.mostrar_analisis_completo(config)

        seleccion = self.pedir_seleccion(config)

        if seleccion is None:
            UtilidadesSistema.pausar()
            return

        cabe = self.analizador.mostrar_analisis_seleccion(
            seleccion=seleccion,
            config=config
        )

        if not cabe:
            UtilidadesSistema.pausar()
            return

        ruta = self.pedir_ruta_archivo(config.carpeta)

        if ruta is None:
            UtilidadesSistema.pausar()
            return

        print("\nCalculando velocidad aproximada...")

        velocidad = self.generador.probar_velocidad(
            caracteres=config.caracteres,
            longitud=config.longitud,
            cantidad=seleccion.cantidad,
            carpeta=config.carpeta
        )

        velocidad_estimada = None

        if velocidad > 0:
            velocidad_estimada = velocidad
            tiempo_estimado = seleccion.cantidad / velocidad

            print(f"Velocidad estimada      : {velocidad:,.0f} combinaciones/s")
            print(f"Tiempo estimado         : {Formateador.tiempo_legible(tiempo_estimado)}")
        else:
            print("No se pudo calcular la velocidad estimada.")

        print(f"Archivo destino         : {ruta}")

        continuar = input("\n¿Deseas continuar? (s/n): ").lower()

        if continuar != "s":
            print("Operación cancelada.")
            UtilidadesSistema.pausar()
            return

        resultado = self.generador.generar_archivo(
            caracteres=config.caracteres,
            longitud=config.longitud,
            cantidad=seleccion.cantidad,
            ruta=ruta
        )

        ruta_reporte = self.reporte.guardar_diccionario_general(
            config=config,
            seleccion=seleccion,
            resultado=resultado,
            velocidad_estimada=velocidad_estimada
        )

        print(f"\nReporte generado        : {ruta_reporte}")

        UtilidadesSistema.pausar()

    def opcion_solo_calcular(self):
        UtilidadesSistema.limpiar_pantalla()
        self.ui.limpiar()
        self.ui.titulo(
            "SOLO CALCULAR / SIMULAR",
            "Analiza combinaciones, peso estimado y espacio sin generar archivo."
        )

        config = self.crear_configuracion_desde_usuario()

        if config is None:
            UtilidadesSistema.pausar()
            return

        self.analizador.mostrar_analisis_completo(config)

        calcular_seleccion = input(
            "\n¿Deseas calcular una selección específica? (s/n): "
        ).lower()

        if calcular_seleccion == "s":
            seleccion = self.pedir_seleccion(config)

            if seleccion is not None:
                self.analizador.mostrar_analisis_seleccion(
                    seleccion=seleccion,
                    config=config,
                    mostrar_muestra=False
                )

        print("\nNo se generó ningún archivo.")
        UtilidadesSistema.pausar()

    def mostrar_ejemplos(self):
        self.ui.limpiar()
        self.ui.titulo(
            "EJEMPLOS DE USO",
            "Casos comunes para decimal, hexadecimal y muestras parciales."
        )

        print("""
Ejemplo decimal:
  Caracteres: 0123456789
  Longitud: 4
  Entrada de cantidad: Enter
  Resultado: 0000 hasta 9999

Ejemplo hexadecimal:
  Caracteres: 0123456789ABCDEF
  Longitud: 8
  Entrada de cantidad: 100mb
  Resultado: genera tantas combinaciones como quepan en 100 MB

Ejemplo rango pequeño:
  Caracteres: 012345
  Longitud: 3
  Entrada de cantidad: Enter
  Total: 6^3 = 216 combinaciones

Ejemplo muestra:
  Caracteres: abc123
  Longitud: 10
  Entrada de cantidad: 1000000
  Resultado: genera solo 1,000,000 combinaciones

Notas:
  - Enter en cantidad significa generar todo.
  - 100 significa 100 combinaciones.
  - 100mb significa generar hasta ocupar aproximadamente 100 MB.
  - También puedes usar kb, mb, gb, tb o pb.
""")

        self.ui.pausa()