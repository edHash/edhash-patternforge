import shutil

from config import (
    ConfiguracionDiccionario,
    CantidadSolicitada,
    SeleccionGeneracion
)
from utilidades import CalculadoraTamano, Formateador


class AnalizadorDiccionario:

    def crear_configuracion(
        self,
        caracteres: str,
        longitud: int,
        carpeta: str
    ) -> ConfiguracionDiccionario:

        total = len(caracteres) ** longitud

        bytes_linea = CalculadoraTamano.bytes_por_linea(
            caracteres,
            longitud
        )

        _, _, espacio_libre = shutil.disk_usage(carpeta)

        maximo_recomendado = int(
            (espacio_libre * 0.90) // bytes_linea
        )

        maximo_recomendado = min(
            maximo_recomendado,
            total
        )

        return ConfiguracionDiccionario(
            caracteres=caracteres,
            longitud=longitud,
            carpeta=carpeta,
            total_combinaciones=total,
            bytes_por_linea=bytes_linea,
            espacio_libre=espacio_libre,
            maximo_recomendado=maximo_recomendado
        )

    def mostrar_analisis_completo(
        self,
        config: ConfiguracionDiccionario
    ):

        tamano_total = CalculadoraTamano.estimar_tamano(
            config.bytes_por_linea,
            config.total_combinaciones
        )

        print("\n" + "=" * 70)
        print("ANÁLISIS DEL DICCIONARIO COMPLETO")
        print("=" * 70)
        print(f"Caracteres únicos       : {len(config.caracteres):,}")
        print(f"Caracteres usados       : {config.caracteres}")
        print(f"Longitud                : {config.longitud:,}")
        print(f"Combinaciones totales   : {config.total_combinaciones:,}")
        print(f"Peso si generas TODO    : {Formateador.tamano_legible(tamano_total)}")
        print(f"Espacio libre en disco  : {Formateador.tamano_legible(config.espacio_libre)}")
        print(f"Peso aprox. por línea   : {config.bytes_por_linea} bytes")

        if tamano_total > config.espacio_libre:
            print("\n⚠️ El diccionario completo NO cabe en esta unidad.")
            print(
                f"Puedes generar aproximadamente hasta "
                f"{config.maximo_recomendado:,} combinaciones "
                f"sin usar más del 90% del espacio libre."
            )
        else:
            print("\n✅ El diccionario completo sí cabe en esta unidad.")

    def crear_seleccion(
        self,
        solicitud: CantidadSolicitada,
        config: ConfiguracionDiccionario
    ) -> SeleccionGeneracion:

        tamano_estimado = CalculadoraTamano.estimar_tamano(
            config.bytes_por_linea,
            solicitud.cantidad
        )

        return SeleccionGeneracion(
            cantidad=solicitud.cantidad,
            modo=solicitud.modo,
            tamano_estimado=tamano_estimado,
            bytes_solicitados=solicitud.bytes_solicitados
        )

    def mostrar_analisis_seleccion(
        self,
        seleccion: SeleccionGeneracion,
        config: ConfiguracionDiccionario,
        mostrar_muestra=True
    ) -> bool:

        print("\n" + "=" * 70)
        print("ANÁLISIS DE TU SELECCIÓN")
        print("=" * 70)
        print(f"Modo                    : {seleccion.modo}")
        print(f"Combinaciones           : {seleccion.cantidad:,}")
        print(f"Peso estimado           : {Formateador.tamano_legible(seleccion.tamano_estimado)}")
        print(f"Espacio libre           : {Formateador.tamano_legible(config.espacio_libre)}")

        if seleccion.bytes_solicitados is not None:
            print(
                f"Peso solicitado         : "
                f"{Formateador.tamano_legible(seleccion.bytes_solicitados)}"
            )

        if seleccion.tamano_estimado > config.espacio_libre:
            print("\n❌ No hay suficiente espacio para esa cantidad.")
            print("La operación fue cancelada para proteger el sistema.")
            print(
                f"\nCantidad máxima aproximada recomendada: "
                f"{config.maximo_recomendado:,}"
            )
            return False

        if seleccion.tamano_estimado > config.espacio_libre * 0.90:
            print(
                "\n⚠️ Advertencia: esta selección usaría más del 90% "
                "del espacio libre disponible."
            )

        if seleccion.modo != "COMPLETO" and mostrar_muestra:
            print(
                "\n⚠️ Se trabajará solo una muestra del total "
                "de combinaciones posibles."
            )

        return True