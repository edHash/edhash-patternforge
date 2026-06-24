from datetime import datetime
import os
from typing import Optional, Sequence
from branding import PROJECT_NAME, PROJECT_VERSION, PROJECT_AUTHOR

from config import (
    ConfiguracionDiccionario,
    SeleccionGeneracion,
    ResultadoArchivo
)
from utilidades import Formateador


class ReporteGeneracion:
    """
    Clase encargada de crear reportes de generación.

    Sirve para:
    - Generador universal de combinaciones
    - Auditoría por área
    """

    def crear_ruta_reporte(
        self,
        ruta_archivo_generado: str,
        prefijo: str
    ) -> str:
        carpeta = os.path.dirname(
            os.path.abspath(ruta_archivo_generado)
        )

        nombre_base = os.path.splitext(
            os.path.basename(ruta_archivo_generado)
        )[0]

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

        nombre_reporte = f"{prefijo}_{nombre_base}_{fecha}.txt"

        return os.path.join(carpeta, nombre_reporte)

    def _fecha_actual(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _seccion(self, archivo, titulo: str):
        archivo.write("\n" + "=" * 70 + "\n")
        archivo.write(titulo + "\n")
        archivo.write("=" * 70 + "\n")

    def _campo(self, archivo, nombre: str, valor):
        archivo.write(f"{nombre:<28}: {valor}\n")

    def _formatear_lista(self, valores: Sequence[str]) -> str:
        resultado = []

        for valor in valores:
            if valor == "":
                resultado.append("[vacío]")
            elif valor == " ":
                resultado.append("[espacio]")
            else:
                resultado.append(valor)

        return ", ".join(resultado)

    def guardar_diccionario_general(
        self,
        config: ConfiguracionDiccionario,
        seleccion: SeleccionGeneracion,
        resultado: ResultadoArchivo,
        velocidad_estimada: Optional[float] = None
    ) -> str:

        ruta_reporte = self.crear_ruta_reporte(
            resultado.ruta_archivo,
            "reporte_diccionario"
        )

        tamano_total = (
            config.total_combinaciones
            * config.bytes_por_linea
        )

        velocidad_promedio = 0

        if resultado.tiempo_segundos > 0:
            velocidad_promedio = (
                resultado.elementos_escritos
                / resultado.tiempo_segundos
            )

        with open(ruta_reporte, "w", encoding="utf-8") as archivo:
            self._seccion(
                archivo,
                "REPORTE DE GENERACIÓN - DICCIONARIO GENERAL"
            )

            self._campo(archivo, "Fecha de generación", self._fecha_actual())
            self._campo(archivo, "Herramienta", PROJECT_NAME)
            self._campo(archivo, "Versión", PROJECT_VERSION)
            self._campo(archivo, "Autor", PROJECT_AUTHOR)
            self._campo(archivo, "Herramienta", PROJECT_NAME)
            self._campo(archivo, "Versión", PROJECT_VERSION)
            self._campo(archivo, "Autor", PROJECT_AUTHOR)
            self._campo(archivo, "Tipo de proceso", "Generador universal")
            self._campo(archivo, "Archivo generado", resultado.ruta_archivo)

            self._seccion(archivo, "CONFIGURACIÓN DEL DICCIONARIO")
            self._campo(archivo, "Caracteres únicos", len(config.caracteres))
            self._campo(archivo, "Caracteres usados", config.caracteres)
            self._campo(archivo, "Longitud", config.longitud)
            self._campo(
                archivo,
                "Combinaciones totales",
                f"{config.total_combinaciones:,}"
            )
            self._campo(
                archivo,
                "Peso si genera TODO",
                Formateador.tamano_legible(tamano_total)
            )
            self._campo(
                archivo,
                "Peso aprox. por línea",
                f"{config.bytes_por_linea} bytes"
            )

            self._seccion(archivo, "ANÁLISIS DE TU SELECCIÓN")
            self._campo(archivo, "Modo", seleccion.modo)
            self._campo(
                archivo,
                "Combinaciones a generar",
                f"{seleccion.cantidad:,}"
            )
            self._campo(
                archivo,
                "Peso estimado",
                Formateador.tamano_legible(seleccion.tamano_estimado)
            )
            self._campo(
                archivo,
                "Espacio libre",
                Formateador.tamano_legible(config.espacio_libre)
            )

            if seleccion.bytes_solicitados is not None:
                self._campo(
                    archivo,
                    "Peso solicitado",
                    Formateador.tamano_legible(
                        seleccion.bytes_solicitados
                    )
                )

            self._seccion(archivo, "RESULTADO FINAL")
            self._campo(
                archivo,
                "Combinaciones escritas",
                f"{resultado.elementos_escritos:,}"
            )
            self._campo(
                archivo,
                "Tiempo real empleado",
                Formateador.tiempo_legible(resultado.tiempo_segundos)
            )
            self._campo(
                archivo,
                "Tamaño real del archivo",
                Formateador.tamano_legible(resultado.tamano_real)
            )
            self._campo(
                archivo,
                "Velocidad promedio",
                f"{velocidad_promedio:,.0f} combinaciones/s"
            )

            if velocidad_estimada is not None:
                self._campo(
                    archivo,
                    "Velocidad estimada previa",
                    f"{velocidad_estimada:,.0f} combinaciones/s"
                )

        return ruta_reporte

    def guardar_auditoria_area(
        self,
        resultado: ResultadoArchivo,
        modo: str,
        patrones_estimados: int,
        patrones_a_generar: int,
        peso_estimado: int,
        espacio_libre: int,
        tokens_base_count: int,
        tokens_finales_count: int,
        separadores: Sequence[str],
        sufijos: Sequence[str],
        max_partes: int,
        bytes_linea: int,
        tamano_total: int,
        peso_solicitado: Optional[int] = None,
        filtro_datos_sensibles: str = "Activado"
    ) -> str:

        ruta_reporte = self.crear_ruta_reporte(
            resultado.ruta_archivo,
            "reporte_auditoria"
        )

        velocidad_promedio = 0

        if resultado.tiempo_segundos > 0:
            velocidad_promedio = (
                resultado.elementos_escritos
                / resultado.tiempo_segundos
            )

        with open(ruta_reporte, "w", encoding="utf-8") as archivo:
            self._seccion(
                archivo,
                "REPORTE DE GENERACIÓN - AUDITORÍA POR ÁREA"
            )

            self._campo(archivo, "Fecha de generación", self._fecha_actual())
            self._campo(archivo, "Tipo de proceso", "Auditoría por área")
            self._campo(archivo, "Archivo generado", resultado.ruta_archivo)
            self._campo(
                archivo,
                "Filtro datos sensibles",
                filtro_datos_sensibles
            )

            self._seccion(archivo, "CONFIGURACIÓN DE AUDITORÍA")
            self._campo(archivo, "Tokens base seguros", tokens_base_count)
            self._campo(archivo, "Tokens finales", tokens_finales_count)
            self._campo(
                archivo,
                "Separadores",
                self._formatear_lista(separadores)
            )
            self._campo(
                archivo,
                "Sufijos",
                self._formatear_lista(sufijos)
            )
            self._campo(archivo, "Máx. tokens por patrón", max_partes)
            self._campo(
                archivo,
                "Patrones estimados",
                f"{patrones_estimados:,}"
            )
            self._campo(
                archivo,
                "Peso si genera TODO",
                Formateador.tamano_legible(tamano_total)
            )
            self._campo(
                archivo,
                "Peso aprox. por línea",
                f"{bytes_linea} bytes"
            )

            self._seccion(archivo, "ANÁLISIS DE TU SELECCIÓN")
            self._campo(archivo, "Modo", modo)
            self._campo(
                archivo,
                "Patrones a generar",
                f"{patrones_a_generar:,}"
            )
            self._campo(
                archivo,
                "Peso estimado",
                Formateador.tamano_legible(peso_estimado)
            )
            self._campo(
                archivo,
                "Espacio libre",
                Formateador.tamano_legible(espacio_libre)
            )

            if peso_solicitado is not None:
                self._campo(
                    archivo,
                    "Peso solicitado",
                    Formateador.tamano_legible(peso_solicitado)
                )

            self._seccion(archivo, "RESULTADO FINAL")
            self._campo(
                archivo,
                "Patrones escritos",
                f"{resultado.elementos_escritos:,}"
            )
            self._campo(
                archivo,
                "Tiempo real empleado",
                Formateador.tiempo_legible(resultado.tiempo_segundos)
            )
            self._campo(
                archivo,
                "Tamaño real del archivo",
                Formateador.tamano_legible(resultado.tamano_real)
            )
            self._campo(
                archivo,
                "Velocidad promedio",
                f"{velocidad_promedio:,.0f} patrones/s"
            )

        return ruta_reporte