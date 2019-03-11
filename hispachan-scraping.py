# -*- coding: utf-8 -*-
import requests, re, sys, os

enlace = re.compile("https?://(www\.)?hispachan\.org/([a-z]+)/res/([0-9]+)\.html")
x, tablon, idpost = enlace.match(sys.argv[1]).groups()
adjuntos = re.compile('<span class="file(?:namereply|size)">[\r\n]+<a[\s\r\n]+target="_blank"[\s\r\n]+href="([^"]+)"(?:[\s\S]*?)<span class="nombrefile"(?:>, ([^<]+)| title="([^"]+))')
peticion = requests.get("https://www.hispachan.org/%s/res/%s.html" % (tablon, idpost))
# Si el hilo aun existe extrae los archivos
if peticion.status_code == 200:
    try: os.makedirs(os.path.join(tablon, idpost))
    except OSError, e:
        if e.errno == os.errno.EEXIST:
            respuesta = raw_input("La carpeta donde se descargaran los archivos ya existe. ¿Desea sobreescribir los archivos? [s/n]: ")
            if respuesta in ["n", "N"]: exit(17)
    for archivo, nombre1, nombre2 in adjuntos.findall(peticion.content):
        nombre = (nombre1 if nombre2 == "" else nombre2)
        print("Descargando %s (%s)" % (archivo, nombre))
        descarga = requests.get(archivo)
        # El archivo basicamente se guarda en tablon/post/nombre
        # Al parecer las imagenes dentro de un spoiler no contienen nombre propio
        # por lo que se usa el timestamp en su lugar
        if nombre == "Spoiler Picture.jpg":
            salida = open(os.path.join(tablon, idpost, archivo.split("/")[-1]), "wb")
        else:
            salida = open(os.path.join(tablon, idpost, nombre), "wb")
        salida.write(descarga.content)
        salida.close()
else: print("El hilo no existe")
