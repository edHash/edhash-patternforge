import re

from config import CantidadSolicitada


class ParserCantidad:
    """
    Esta clase solo interpreta texto.
    No imprime, no pide input y no sabe nada del menú.

    Ejemplos:
    Enter  -> generar todo
    100    -> 100 combinaciones
    100mb  -> tantas combinaciones como quepan en 100 MB
    1gb    -> tantas combinaciones como quepan en 1 GB
    """

    def convertir_numero_local(self, texto: str) -> float:
        texto = texto.strip().replace("_", "")

        if "," in texto and "." not in texto:
            partes = texto.split(",")

            if len(partes[-1]) == 3 and len(partes) > 1:
                texto = texto.replace(",", "")
            else:
                texto = texto.replace(",", ".")

        elif "," in texto and "." in texto:
            texto = texto.replace(",", "")

        return float(texto)

    def parsear_tamano_a_bytes(self, texto: str):
        texto = texto.strip().lower().replace(" ", "")

        patron = r"^([0-9]+(?:[.,][0-9]+)?)((?:k|m|g|t|p)?b|bytes?)$"
        coincidencia = re.match(patron, texto)

        if not coincidencia:
            return None

        numero_texto = coincidencia.group(1)
        unidad = coincidencia.group(2)

        numero = self.convertir_numero_local(numero_texto)

        unidades = {
            "b": 1,
            "byte": 1,
            "bytes": 1,
            "kb": 1024,
            "mb": 1024 ** 2,
            "gb": 1024 ** 3,
            "tb": 1024 ** 4,
            "pb": 1024 ** 5,
        }

        return int(numero * unidades[unidad])

    def parsear(
        self,
        entrada: str,
        total: int,
        bytes_linea: int
    ) -> CantidadSolicitada:

        entrada = entrada.strip().lower()

        if entrada == "":
            return CantidadSolicitada(
                cantidad=total,
                modo="COMPLETO",
                bytes_solicitados=None
            )

        bytes_solicitados = self.parsear_tamano_a_bytes(entrada)

        if bytes_solicitados is not None:
            combinaciones = bytes_solicitados // bytes_linea

            if combinaciones <= 0:
                raise ValueError(
                    "El tamaño indicado no alcanza ni para una combinación."
                )

            if combinaciones > total:
                combinaciones = total

            return CantidadSolicitada(
                cantidad=combinaciones,
                modo="POR PESO",
                bytes_solicitados=bytes_solicitados
            )

        entrada_limpia = entrada.replace(",", "").replace("_", "")

        if entrada_limpia.isdigit():
            combinaciones = int(entrada_limpia)

            if combinaciones <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")

            if combinaciones > total:
                combinaciones = total

            return CantidadSolicitada(
                cantidad=combinaciones,
                modo="POR CANTIDAD",
                bytes_solicitados=None
            )

        raise ValueError(
            "Formato inválido. Usa algo como 100, 1000000, 100mb, 1gb o 1.5gb."
        )