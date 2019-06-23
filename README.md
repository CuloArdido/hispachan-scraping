# Web-Scraping (Node.js)

## Descripción

Web Scraping a hispachan, con node.js utilizando cheerio y yargs  
No me hago responsable por el mal uso o daños a otros realizados por esta herramienta

## Instalación
`npm i`

## Dependencias

`"cheerio": "1.0.0-rc.2", "request": "2.88.0" "yargs": "12.0.5"`

## Uso
#### Linux
`sudo chmod +x index.js`  
`sudo ./index.js --tablon={tablon} --hilo={hilo}`  
`Ejemplo: sudo ./index.js --tablon=di --hilo=50859`  

#### Windows
Para usar en windows debes modificar el archivo package.json en la linea 8 con el tablón y el hilo que quieres descargar, luego ejecutar `npm run win`

## Bugs conocidos:
No descarga los videos, los selecciona pero aun no los maneja

---
# hispachan-scraping.py
## Descripción
Versión del scrapper hecha en Python. Actualmente se encuentra en [esta rama](../../tree/python).
## Dependencias
Python 2 o 3 (no requiere módulos adicionales).
## Uso

```
Uso: hispachan-scraping.py [-h] [-n] [-o] [-u] [-d] url [destino]

Descarga los archivos adjuntos de un hilo de Hispachan.

Argumentos posicionales:
  url                Enlace del hilo o identificador en la forma
                     "tablón/hilo".
  destino            Directorio en donde se guardaran los archivos (por
                     defecto se descargan en el directorio actual).

Argumentos opcionales:
  -h, -help          Muestra este mensaje de ayuda y sale.
  -n, -no-subfolder  Omite la creación de una subcarpeta para las imágenes.
  -o, -overwrite     Sobrescribe los archivos con el mismo nombre.
  -u, -update        Solo descarga los archivos que no existen.
  -d, -debug         Dispara las excepciones para facilitar la detección de
                     bugs.
```

## Bugs conocidos
Ninguno por ahora, pero faltaría hacer mas pruebas con la expresión regular que detecta enlaces y nombres reales de los archivos.

## Por hacer
☑ Agregar un modo de depuración/verbose (al menos para mostrar mas detalles cuando se da una excepción).

☑ Hacer que funcione en Python 2.

☐ Agregar soporte para descargar desde varios hilos a la vez (ya sea en la consola o a través de un archivo).

☐ Quizás crear una interfaz gráfica y/o una webapp (esto ultimo podría ser con Django o Flask).
