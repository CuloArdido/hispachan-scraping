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
Versión simplificada del scrapper hecha en Python.
## Uso
`python hispachan-scraping.py enlace_hilo`
## Bugs conocidos
Ninguno por ahora, pero faltaría afinar el manejo de excepciones y hacer mas pruebas con la expresión regular que detecta enlaces y nombres reales de los archivos.
