# edHash Dictionary Forge

> Creador de diccionarios personalizados para auditoría, análisisy generación de patrones.

```text
[ edHash Security Lab ]
[ Mode: Local Analysis ]
[ Network Access: Disabled ]
[ Purpose: Authorized Auditing / Education ]
```

---

## Descripción

**edHash Dictionary Forge** es una herramienta de consola desarrollada en Python para generar diccionarios personalizados, combinaciones y patrones(PASSWORD) derivados de información proporcionada por el usuario.

El proyecto nace como una práctica técnica para comprender cómo los datos simples, las combinaciones y los patrones humanos pueden influir en la seguridad de credenciales.

No rompe sistemas.
No se conecta a servicios externos.
No prueba contraseñas contra cuentas reales.

Su propósito es generar archivos de texto bajo parámetros definidos por el usuario, dentro de entornos, laboratorios controlados o auditorías.

```text
La herramienta no ataca.
La herramienta revela patrones.
El riesgo aparece cuando esos patrones ya existen en la vida real.
```

---

## Objetivo del proyecto

El objetivo principal es automatizar la generación de diccionarios personalizados de forma controlada, permitiendo analizar cómo pequeñas piezas de información pueden transformarse en combinaciones predecibles.

La herramienta permite definir:

* Caracteres permitidos.
* Longitud mínima y máxima.
* Cantidad exacta de patrones.
* Tamaño aproximado del archivo generado.
* Carpeta y nombre del archivo de salida.
* Datos personalizados para auditoría.
* Estimación previa de peso.
* Validación de espacio disponible.
* Reporte final de generación.

Este proyecto combina programación, combinatoria, manejo de archivos, validación de entradas y fundamentos de seguridad defensiva.

---

## Características principales

```text
[ CORE FEATURES ]
```

* Generación general de combinaciones.
* Soporte para números, letras y símbolos personalizados.
* Soporte para modo hexadecimal.
* Definición de longitud mínima y máxima.
* Generación por cantidad exacta de patrones.
* Generación por tamaño aproximado del archivo.
* Estimación previa de combinaciones posibles.
* Estimación aproximada del peso final.
* Validación de espacio disponible antes de generar.
* Barra de progreso durante la generación.
* Cálculo aproximado de tiempo de ejecución.
* Selección de carpeta y nombre del archivo de salida.
* Módulo de auditoría basado en datos proporcionados por el usuario.
* Reporte final con resumen técnico.
* Interfaz por consola organizada mediante menú principal.

---

## Módulos principales

### 1. Generación general

Permite crear combinaciones a partir de caracteres definidos manualmente por el usuario.

Ejemplos de conjuntos posibles:

```text
0123456789
abcdef
ABCDEF0123456789
abc123!@#
```

El usuario puede definir la longitud de las combinaciones y limitar la salida por cantidad exacta o por tamaño aproximado.

```text
Input  -> caracteres, longitud, límite
Process -> combinaciones controladas
Output -> diccionario local en archivo .txt
```

---

### 2. Auditoría

El módulo de auditoría genera patrones a partir de información proporcionada por el usuario, como nombres, apodos, fechas, palabras clave u otros datos.

Este módulo está pensado para demostrar cómo ciertos datos personales o contextuales pueden convertirse en patrones débiles cuando se usan de forma directa o predecible dentro de una contraseña.

```text
[ AUDIT MODE ]

Data entered by user
        ↓
Pattern generation
        ↓
Local dictionary
        ↓
Security awareness
```

---

### 3. Reporte final

Al terminar una generación, la herramienta muestra un resumen con información útil para documentar prácticas o auditorías internas.

El reporte puede incluir:

* Modo utilizado.
* Cantidad de patrones generados.
* Archivo de salida.
* Peso aproximado.
* Tiempo estimado o tiempo utilizado.
* Parámetros principales de generación.
* Ruta donde fue guardado el resultado.

---

## Requisitos

```text
[ SYSTEM REQUIREMENTS ]
```

* Python 3.10 o superior.
* Sistema operativo compatible con Python.
* Terminal o consola de comandos.
* Espacio disponible según el tamaño del diccionario generado.

No se requiere conexión a internet.

---

## Ejecución

Clona o descarga el proyecto y entra a la carpeta principal.

Ejecuta:

```bash
python main.py
```

En algunos sistemas puede ser necesario usar:

```bash
python3 main.py
```

---

## Uso básico

Al iniciar la herramienta se mostrará un menú principal con las opciones disponibles.

Flujo general:

```text
1. Seleccionar modo de generación.
2. Definir caracteres o datos de auditoría.
3. Elegir longitud, cantidad o tamaño objetivo.
4. Seleccionar nombre y ubicación del archivo.
5. Revisar estimaciones.
6. Confirmar generación.
7. Obtener archivo y reporte final.
```

---

## Ejemplo educativo

Un usuario puede generar combinaciones numéricas de longitud definida para comprender cuántos patrones existen en un rango pequeño.

También puede utilizar el módulo de auditoría para observar cómo datos simples pueden convertirse en combinaciones predecibles.

```text
No se trata de adivinar secretos.
Se trata de entender por qué algunos secretos nunca fueron realmente secretos.
```

---

## Uso responsable

Esta herramienta fue creada únicamente para:

* Prácticas educativas.
* Laboratorios propios.
* Auditorías internas autorizadas.
* Análisis de patrones.
* Demostraciones de seguridad defensiva.
* Comprensión de combinatoria aplicada.
* Concientización sobre contraseñas débiles.

```text
[ ETHICAL BOUNDARY ]

Autorización primero.
Análisis después.
```

---

## Recomendaciones de seguridad

No se recomienda subir a repositorios públicos:

* Diccionarios generados.
* Datos personales reales.
* Reportes con información sensible.
* Archivos grandes de salida.
* Evidencia de auditorías reales sin autorización.
* Listas relacionadas con personas, empresas o sistemas reales.

Se recomienda mantener los archivos generados fuera del repositorio o ignorarlos mediante `.gitignore`.

Ejemplo:

```gitignore
salidas/
reportes/
diccionarios/
*.txt
*.log
```

---

## Tecnologías utilizadas

```text
[ STACK ]
```

* Python
* Programación orientada a objetos
* Manejo de archivos
* Validación de entradas
* Cálculo de combinaciones
* Generación controlada de patrones
* Interfaz por consola
* Documentación técnica

---

## Estado del proyecto

```text
[ PROJECT STATUS ]

Version: Stable Lab Build
Execution: Local
Network: Disabled
External Testing: Not included
```

El proyecto se encuentra en una versión estable para laboratorio, demostración y portafolio técnico.

Posibles mejoras futuras:

* Exportación avanzada de reportes.
* Perfiles de auditoría guardados.
* Más reglas de combinación.
* Mejoras visuales en consola.
* Módulos de análisis estadístico.
* Separación completa por paquetes.
* Pruebas unitarias.
* Documentación extendida.

---

## Autor

Proyecto desarrollado por **edHash** como parte de un portafolio técnico enfocado en programación, soporte técnico, seguridad defensiva y análisis de sistemas.

```text
edHash
Software Development | IT Support | Defensive Security Learning
```

A veces, la llave de tus secretos digitales está escondida en la información que tú mismo dejaste expuesta.