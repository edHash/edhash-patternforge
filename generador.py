from itertools import product, islice
import os
import tempfile
import time

from utilidades import Formateador
from progreso import BarraProgreso
from config import ResultadoArchivo


class GeneradorCombinaciones:

    def probar_velocidad(
        self,
        caracteres: str,
        longitud: int,
        cantidad: int,
        carpeta: str
    ):
        muestra = min(cantidad, 50000)

        if muestra <= 0:
            return 0

        archivo_temp = None

        try:
            temp = tempfile.NamedTemporaryFile(
                delete=False,
                dir=carpeta,
                prefix="prueba_velocidad_",
                suffix=".tmp",
                mode="w",
                encoding="utf-8",
                newline="\n"
            )

            archivo_temp = temp.name
            inicio = time.time()

            with temp as archivo:
                generador = product(caracteres, repeat=longitud)

                for combinacion in islice(generador, muestra):
                    archivo.write("".join(combinacion) + "\n")

            fin = time.time()
            tiempo = fin - inicio

            if tiempo <= 0:
                return 0

            return muestra / tiempo

        finally:
            if archivo_temp and os.path.exists(archivo_temp):
                os.remove(archivo_temp)

    def generar_archivo(
        self,
        caracteres: str,
        longitud: int,
        cantidad: int,
        ruta: str
    ):
        print("\nGenerando archivo...\n")

        barra = BarraProgreso(cantidad)
        intervalo_progreso = BarraProgreso.calcular_intervalo(cantidad)

        contador = 0

        with open(
            ruta,
            "w",
            encoding="utf-8",
            newline="\n"
        ) as archivo:

            generador = product(caracteres, repeat=longitud)

            for combinacion in islice(generador, cantidad):
                archivo.write("".join(combinacion) + "\n")
                contador += 1

                if contador % intervalo_progreso == 0:
                    barra.mostrar(contador)

            barra.mostrar(contador)

        tiempo_total = barra.tiempo_transcurrido()
        tamano_real = os.path.getsize(ruta)

        print("\n\n" + "=" * 70)
        print("✅ PROCESO FINALIZADO")
        print("=" * 70)
        print(f"Combinaciones escritas  : {contador:,}")
        print(f"Tiempo real empleado    : {Formateador.tiempo_legible(tiempo_total)}")
        print(f"Tamaño real del archivo : {Formateador.tamano_legible(tamano_real)}")
        print(f"Archivo generado        : {ruta}")
        return ResultadoArchivo(
            ruta_archivo=ruta,
            elementos_escritos=contador,
            tiempo_segundos=tiempo_total,
            tamano_real=tamano_real,
            nombre_elemento="combinaciones")