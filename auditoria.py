from itertools import product, islice
import os
import re
import shutil
import time
from typing import List, Optional, Tuple

from selector_cantidad import SelectorCantidad
from utilidades import UtilidadesSistema, Formateador
from progreso import BarraProgreso
from reporte import ReporteGeneracion
from config import ResultadoArchivo



class ModuloAuditoriaArea:
    """
    Genera patrones institucionales para auditoría interna autorizada.

    No está pensado para usar datos personales de empleados.
    """

    def __init__(self):
        self.selector_cantidad = SelectorCantidad()
        self.reporte = ReporteGeneracion()

    def ejecutar(self):
        UtilidadesSistema.limpiar_pantalla()

        print("=" * 70)
        print(" AUDITORÍA POR ÁREA ")
        print("=" * 70)
        print(
                "\n   Audit Mode forja patrones y genera diccionarios personalizados\n"
                "usando datos personales como: nombres, apodos, fechas importantes, etc.\n"
                "           TU INFORMACIÓN ES TU ESLABÓN DÉBIL-EDHASH\n"
        )

        aceptar = input("PARA CONTINUAR[S]: ").strip().upper()

        if aceptar != "S":
            print("Opcion invalida")
            UtilidadesSistema.pausar()
            return

        carpeta = self.pedir_carpeta()

        if carpeta is None:
            UtilidadesSistema.pausar()
            return

        tokens_base = self.pedir_tokens_por_preguntas()

        if not tokens_base:
            print("❌ No se ingresaron tokens base.")
            UtilidadesSistema.pausar()
            return

        tokens_base = self.expandir_tokens(tokens_base)

        if not tokens_base:
            print("❌ Todos los tokens fueron bloqueados por seguridad.")
            UtilidadesSistema.pausar()
            return

        aplicar_variantes = input(
            "\n¿Aplicar variantes de mayúsculas/minúsculas? (s/n) [s]: "
        ).strip().lower()

        if aplicar_variantes in ("", "s", "si", "sí"):
            tokens = self.aplicar_variantes_texto(tokens_base)
        else:
            tokens = self.unicos(tokens_base)

        separadores = self.pedir_lista_especial(
            "\nSeparadores separados por coma [vacio,_,.,-]: ",
            defecto=["", "_", ".", "-"]
        )

        sufijos = self.pedir_lista_especial(
            "Sufijos o símbolos separados por coma [vacio,!,@,#]: ",
            defecto=["", "!", "@", "#"]
        )

        max_partes = self.pedir_entero(
            "Máximo de tokens por patrón (1-3 recomendado) [2]: ",
            defecto=2,
            minimo=1,
            maximo=3
        )

        total_estimado = self.calcular_total_estimado(
            total_tokens=len(tokens),
            total_separadores=len(separadores),
            total_sufijos=len(sufijos),
            max_partes=max_partes
        )

        bytes_linea = self.estimar_bytes_linea_por_muestra(
            tokens=tokens,
            separadores=separadores,
            sufijos=sufijos,
            max_partes=max_partes
        )

        tamano_total = total_estimado * bytes_linea

        _, _, libre = shutil.disk_usage(carpeta)

        maximo_recomendado = int((libre * 0.90) // bytes_linea)
        maximo_recomendado = min(maximo_recomendado, total_estimado)

        print("\n" + "=" * 70)
        print("ANÁLISIS DEL MODO AUDITORÍA")
        print("=" * 70)
        print(f"Tokens base seguros     : {len(tokens_base):,}")
        print(f"Tokens con variantes    : {len(tokens):,}")
        print(f"Separadores             : {len(separadores):,}")
        print(f"Sufijos                 : {len(sufijos):,}")
        print(f"Máx. tokens por patrón  : {max_partes}")
        print(f"Patrones estimados      : {total_estimado:,}")
        print(f"Peso si generas TODO    : {Formateador.tamano_legible(tamano_total)}")
        print(f"Espacio libre           : {Formateador.tamano_legible(libre)}")
        print(f"Peso aprox. por línea   : {bytes_linea} bytes")

        if tamano_total > libre:
            print("\n⚠️ El conjunto completo NO cabe en esta unidad.")
            print(
                f"Cantidad máxima aproximada recomendada: "
                f"{maximo_recomendado:,} patrones"
            )
        else:
            print("\n✅ El conjunto completo sí cabe en esta unidad.")

        solicitud = self.selector_cantidad.pedir(
            total=total_estimado,
            bytes_linea=bytes_linea,
            nombre_unidad="patrones",
            pregunta="\n¿Cuántos patrones deseas usar?: "
        )

        if solicitud is None:
            UtilidadesSistema.pausar()
            return

        tamano_estimado = solicitud.cantidad * bytes_linea

        print("\n" + "=" * 70)
        print("ANÁLISIS DE TU SELECCIÓN")
        print("=" * 70)
        print(f"Modo                    : {solicitud.modo}")
        print(f"Patrones a generar      : {solicitud.cantidad:,}")
        print(f"Peso estimado           : {Formateador.tamano_legible(tamano_estimado)}")
        print(f"Espacio libre           : {Formateador.tamano_legible(libre)}")

        if solicitud.bytes_solicitados is not None:
            print(
                f"Peso solicitado         : "
                f"{Formateador.tamano_legible(solicitud.bytes_solicitados)}"
            )

        if tamano_estimado > libre:
            print("\n❌ No hay suficiente espacio para esa selección.")
            print(
                f"Cantidad máxima aproximada recomendada: "
                f"{maximo_recomendado:,} patrones"
            )
            UtilidadesSistema.pausar()
            return

        if solicitud.modo != "COMPLETO":
            print(
                "\n⚠️ Se generará solo una muestra del total "
                "de patrones posibles."
            )

        ruta = self.pedir_ruta_archivo(carpeta)

        if ruta is None:
            UtilidadesSistema.pausar()
            return

        continuar = input("\n¿Deseas generar el archivo? (s/n): ").strip().lower()

        if continuar != "s":
            print("Operación cancelada.")
            UtilidadesSistema.pausar()
            return

        resultado = self.generar_archivo_auditoria(
            ruta=ruta,
            tokens=tokens,
            separadores=separadores,
            sufijos=sufijos,
            max_partes=max_partes,
            cantidad=solicitud.cantidad,
            limite_bytes=solicitud.bytes_solicitados
        )

        ruta_reporte = self.reporte.guardar_auditoria_area(
            resultado=resultado,
            modo=solicitud.modo,
            patrones_estimados=total_estimado,
            patrones_a_generar=solicitud.cantidad,
            peso_estimado=tamano_estimado,
            espacio_libre=libre,
            tokens_base_count=len(tokens_base),
            tokens_finales_count=len(tokens),
            separadores=separadores,
            sufijos=sufijos,
            max_partes=max_partes,
            bytes_linea=bytes_linea,
            tamano_total=tamano_total,
            peso_solicitado=solicitud.bytes_solicitados,
            filtro_datos_sensibles="Activado"
        )

        print(f"\nReporte generado        : {ruta_reporte}")

        UtilidadesSistema.pausar()

    def pedir_carpeta(self):
        carpeta = input(
            "\nCarpeta donde guardar el archivo "
            "(Enter = carpeta actual): "
        ).strip()

        carpeta = UtilidadesSistema.normalizar_carpeta(carpeta)

        if not UtilidadesSistema.carpeta_valida(carpeta):
            print("❌ La carpeta indicada no existe o no es válida.")
            return None

        return carpeta

    def pedir_tokens_por_preguntas(self) -> List[str]:
        tokens = []

        area = input("\nÁrea/departamento autorizado: ").strip()

        sistema = input(
            "Sistema, proyecto o servicio relacionado (opcional): "
        ).strip()

        siglas = input(
            "Siglas autorizadas del área/sistema "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        sede_region = input(
            "Sede, región o país institucional autorizado "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        palabras = input(
            "Palabras institucionales separadas por coma (opcional): "
        ).strip()

        periodos = input(
            "Años, ciclos o periodos autorizados separados por coma "
            "(ej. 2025,2026,Q1): "
        ).strip()

        nombre = input(
            "¿Cuál es tu nombre? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        apellido = input(
            "¿Cuál es tu apellido? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        iniciales = input(
            "¿Cuáles son tus iniciales? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        apodo = input(
            "¿Cuál es tu apodo o sobrenombre? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        fecha_nacimiento = input(
            "¿Cuál es tu fecha de nacimiento? "
            "(ej. 15/08/2000) (opcional): "
        ).strip()

        anio_nacimiento = input(
            "¿En qué año naciste? (opcional): "
        ).strip()

        edad_actual = input(
            "¿Cuál es tu edad actual? (opcional): "
        ).strip()

        telefono = input(
            "¿Cuál es tu número de teléfono? (opcional): "
        ).strip()

        identificacion = input(
            "¿Cuál es tu número de empleado, matrícula o identificación? "
            "(opcional): "
        ).strip()

        ciudad_nacimiento = input(
            "¿Cuál es tu ciudad de nacimiento? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        localidad = input(
            "¿Cuál es el nombre de la colonia o localidad donde vives? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        escuela = input(
            "¿Cuál es el nombre de tu escuela o universidad? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        empresa = input(
            "¿Cuál es el nombre de la empresa o institución donde trabajas? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        equipo_deportivo = input(
            "¿Cuál es tu equipo deportivo favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        artista_favorito = input(
            "¿Cuál es tu cantante o artista favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        pelicula_serie = input(
            "¿Cuál es tu película, serie o personaje favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        videojuego = input(
            "¿Qué videojuegos juegas frecuentemente o son tus favoritos? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        pareja = input(
            "¿Cuál es el nombre de tu pareja? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        esposo_esposa = input(
            "¿Cuál es el nombre de tu esposo o esposa? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        novio_novia = input(
            "¿Cuál es el nombre de tu novio o novia? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        hijos = input(
            "¿Cuáles son los nombres de tus hijos? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        padres = input(
            "¿Cuáles son los nombres de tus padres? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        hermanos = input(
            "¿Cuáles son los nombres de tus hermanos? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        familiar_cercano = input(
            "¿Cuál es el nombre de algún familiar cercano? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        fecha_familiar = input(
            "¿Cuál es una fecha importante de un familiar "
            "(cumpleaños, aniversario, etc.)? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        mascota = input(
            "¿Cuál es el nombre de tu mascota? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        mascota_anterior = input(
            "¿Cuál fue el nombre de una mascota anterior? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        raza_mascota = input(
            "¿Cuál es la raza de tu mascota? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        color_favorito = input(
            "¿Cuál es tu color favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        comida_favorita = input(
            "¿Cuál es tu comida favorita? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        lugar_favorito = input(
            "¿Cuál es tu lugar favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        marca_favorita = input(
            "¿Cuál es tu automóvil o marca favorita? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        palabra_frecuente = input(
            "¿Hay alguna palabra que uses frecuentemente? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        anio_actual = input(
            "¿Cuál es el año actual o un año importante para ti? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        anio_ingreso = input(
            "¿En qué año entraste a la escuela o al trabajo? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        fecha_importante = input(
            "¿Cuál es una fecha importante para ti? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        mes_importante = input(
            "¿Cuál es un mes importante para ti? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        cumple_cercano = input(
            "¿Cuál es la fecha de cumpleaños de alguien cercano? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        correo = input(
            "¿Cuál es tu correo electrónico? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        usuario = input(
            "¿Cuál es tu nombre de usuario más utilizado? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        apodo_internet = input(
            "¿Qué alias o nickname usas en internet? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        equipo_futbol = input(
            "¿Cuál es tu equipo de fútbol favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()

        numero_favorito = input(
            "¿Cuál es tu número favorito? "
            "(opcional, puedes ingresar múltiples valores separados por comas): "
        ).strip()
        for valor in [
                        area,
                        sistema,
                        siglas,
                        sede_region,
                        palabras,
                        periodos,
                        nombre,
                        apellido,
                        iniciales,
                        apodo,
                        fecha_nacimiento,
                        anio_nacimiento,
                        edad_actual,
                        telefono,
                        identificacion,
                        correo,
                        usuario,
                        apodo_internet,
                        ciudad_nacimiento,
                        localidad,
                        escuela,
                        empresa,
                        equipo_deportivo,
                        equipo_futbol,
                        artista_favorito,
                        pelicula_serie,
                        videojuego,
                        pareja,
                        esposo_esposa,
                        novio_novia,
                        hijos,
                        padres,
                        hermanos,
                        familiar_cercano,
                        fecha_familiar,
                        mascota,
                        mascota_anterior,
                        raza_mascota,
                        color_favorito,
                        comida_favorita,
                        lugar_favorito,
                        marca_favorita,
                        numero_favorito,
                        palabra_frecuente,
                        anio_actual,
                        anio_ingreso,
                        fecha_importante,
                        mes_importante,
                        cumple_cercano,
                    ]:
            if valor:
                tokens.append(valor)

        tokens.extend(self.separar_por_comas(palabras))
        tokens.extend(self.separar_por_comas(siglas))
        tokens.extend(self.separar_por_comas(sede_region))
        tokens.extend(self.separar_por_comas(periodos))

        tokens.extend(self.separar_por_comas(nombre))
        tokens.extend(self.separar_por_comas(apellido))
        tokens.extend(self.separar_por_comas(iniciales))
        tokens.extend(self.separar_por_comas(apodo))

        tokens.extend(self.separar_por_comas(ciudad_nacimiento))
        tokens.extend(self.separar_por_comas(localidad))
        tokens.extend(self.separar_por_comas(escuela))
        tokens.extend(self.separar_por_comas(empresa))

        tokens.extend(self.separar_por_comas(equipo_deportivo))
        tokens.extend(self.separar_por_comas(equipo_futbol))
        tokens.extend(self.separar_por_comas(artista_favorito))
        tokens.extend(self.separar_por_comas(pelicula_serie))
        tokens.extend(self.separar_por_comas(videojuego))

        tokens.extend(self.separar_por_comas(correo))
        tokens.extend(self.separar_por_comas(usuario))
        tokens.extend(self.separar_por_comas(apodo_internet))

        tokens.extend(self.separar_por_comas(pareja))
        tokens.extend(self.separar_por_comas(esposo_esposa))
        tokens.extend(self.separar_por_comas(novio_novia))
        tokens.extend(self.separar_por_comas(hijos))
        tokens.extend(self.separar_por_comas(padres))
        tokens.extend(self.separar_por_comas(hermanos))
        tokens.extend(self.separar_por_comas(familiar_cercano))

        tokens.extend(self.separar_por_comas(fecha_familiar))

        tokens.extend(self.separar_por_comas(mascota))
        tokens.extend(self.separar_por_comas(mascota_anterior))
        tokens.extend(self.separar_por_comas(raza_mascota))

        tokens.extend(self.separar_por_comas(color_favorito))
        tokens.extend(self.separar_por_comas(comida_favorita))
        tokens.extend(self.separar_por_comas(lugar_favorito))
        tokens.extend(self.separar_por_comas(marca_favorita))
        tokens.extend(self.separar_por_comas(numero_favorito))
        tokens.extend(self.separar_por_comas(palabra_frecuente))

        tokens.extend(self.separar_por_comas(anio_actual))
        tokens.extend(self.separar_por_comas(anio_ingreso))
        tokens.extend(self.separar_por_comas(fecha_importante))
        tokens.extend(self.separar_por_comas(mes_importante))
        tokens.extend(self.separar_por_comas(cumple_cercano))

        return self.unicos(tokens)

    def separar_por_comas(self, texto: str) -> List[str]:
        if not texto:
            return []

        return [
            parte.strip()
            for parte in texto.split(",")
            if parte.strip()
        ]

    def pedir_lista_especial(self, mensaje: str, defecto: List[str]) -> List[str]:
        entrada = input(mensaje).strip()

        if entrada == "":
            return defecto

        resultado = []

        for parte in entrada.split(","):
            valor = parte.strip()

            if valor.lower() in ("vacio", "vacío", "sin", "none", "ninguno"):
                valor = ""

            elif valor.lower() in ("espacio", "space"):
                valor = " "

            resultado.append(valor)

        resultado = self.unicos(resultado)

        if not resultado:
            return defecto

        return resultado

    def pedir_entero(
        self,
        mensaje: str,
        defecto: int,
        minimo: int,
        maximo: int
    ) -> int:
        entrada = input(mensaje).strip()

        if entrada == "":
            return defecto

        try:
            valor = int(entrada)

        except ValueError:
            print(f"Valor inválido. Se usará {defecto}.")
            return defecto

        if valor < minimo:
            return minimo

        if valor > maximo:
            print(f"Por seguridad se limitará a {maximo}.")
            return maximo

        return valor

    def expandir_tokens(self, tokens: List[str]) -> List[str]:
        expandidos = []

        for token in tokens:
            limpio = " ".join(token.strip().split())

            if not limpio:
                continue

            expandidos.append(limpio)

            if " " in limpio:
                sin_espacios = limpio.replace(" ", "")
                con_guion_bajo = limpio.replace(" ", "_")
                iniciales = "".join(
                    palabra[0]
                    for palabra in limpio.split()
                    if palabra
                )

                expandidos.extend([
                    sin_espacios,
                    con_guion_bajo,
                    iniciales
                ])

        return self.unicos(expandidos)


    def aplicar_variantes_texto(self, tokens: List[str]) -> List[str]:
        variantes = []

        for token in tokens:
            variantes.append(token)
            variantes.append(token.lower())
            variantes.append(token.upper())
            variantes.append(token.capitalize())

        return self.unicos(variantes)

    def calcular_total_estimado(
        self,
        total_tokens: int,
        total_separadores: int,
        total_sufijos: int,
        max_partes: int
    ) -> int:
        total = 0

        for partes in range(1, max_partes + 1):
            if partes == 1:
                total += total_tokens
            else:
                total += (total_tokens ** partes) * total_separadores

        return total * total_sufijos

    def iterar_patrones(
        self,
        tokens: List[str],
        separadores: List[str],
        sufijos: List[str],
        max_partes: int
    ):
        for partes in range(1, max_partes + 1):
            separadores_actuales = [""] if partes == 1 else separadores

            for combinacion in product(tokens, repeat=partes):
                for separador in separadores_actuales:
                    base = separador.join(combinacion)

                    for sufijo in sufijos:
                        yield base + sufijo

    def estimar_bytes_linea_por_muestra(
        self,
        tokens: List[str],
        separadores: List[str],
        sufijos: List[str],
        max_partes: int
    ) -> int:
        muestra_maxima = 3000
        total_bytes = 0
        total_lineas = 0

        generador = self.iterar_patrones(
            tokens=tokens,
            separadores=separadores,
            sufijos=sufijos,
            max_partes=max_partes
        )

        for patron in islice(generador, muestra_maxima):
            total_bytes += len((patron + "\n").encode("utf-8"))
            total_lineas += 1

        if total_lineas == 0:
            return 1

        promedio = total_bytes / total_lineas
        return max(1, int(promedio + 0.9999))

    def pedir_ruta_archivo(self, carpeta: str):
        nombre = input("\nNombre del archivo sin .txt: ").strip()

        if nombre == "":
            nombre = "auditoria_area"

        nombre += ".txt"

        ruta = os.path.join(carpeta, nombre)

        if os.path.exists(ruta):
            sobrescribir = input(
                "\n⚠️ El archivo ya existe. "
                "¿Deseas sobrescribirlo? (s/n): "
            ).strip().lower()

            if sobrescribir != "s":
                print("Operación cancelada.")
                return None

        return ruta

    def generar_archivo_auditoria(
        self,
        ruta: str,
        tokens: List[str],
        separadores: List[str],
        sufijos: List[str],
        max_partes: int,
        cantidad: int,
        limite_bytes: Optional[int] = None
    ):
        print("\nGenerando archivo de auditoría...\n")

        barra = BarraProgreso(cantidad)
        intervalo = BarraProgreso.calcular_intervalo(cantidad)

        contador = 0
        bytes_escritos = 0

        with open(
            ruta,
            "w",
            encoding="utf-8",
            newline="\n"
        ) as archivo:

            for patron in self.iterar_patrones(
                tokens=tokens,
                separadores=separadores,
                sufijos=sufijos,
                max_partes=max_partes
            ):
                if contador >= cantidad:
                    break

                linea = patron + "\n"
                bytes_linea = len(linea.encode("utf-8"))

                if (
                    limite_bytes is not None
                    and bytes_escritos + bytes_linea > limite_bytes
                ):
                    break

                archivo.write(linea)
                contador += 1
                bytes_escritos += bytes_linea

                if contador % intervalo == 0:
                    barra.mostrar(contador)

            barra.mostrar(contador)

        tiempo_total = barra.tiempo_transcurrido()
        tamano_real = os.path.getsize(ruta)

        print("\n\n" + "=" * 70)
        print("✅ ARCHIVO DE AUDITORÍA GENERADO")
        print("=" * 70)
        print(f"Patrones escritos       : {contador:,}")
        print(f"Tiempo real empleado    : {Formateador.tiempo_legible(tiempo_total)}")
        print(f"Tamaño real del archivo : {Formateador.tamano_legible(tamano_real)}")
        print(f"Archivo generado        : {ruta}")

        return ResultadoArchivo(
            ruta_archivo=ruta,
            elementos_escritos=contador,
            tiempo_segundos=tiempo_total,
            tamano_real=tamano_real,
            nombre_elemento="patrones"
        )

    def unicos(self, elementos: List[str]) -> List[str]:
        return list(dict.fromkeys(elementos))