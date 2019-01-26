import requests, re, sys, os

enlace = re.compile("https?://(www\.)?hispachan\.org/([a-z]+)/res/([0-9]+)\.html")
x, tablon, idpost = enlace.match(sys.argv[1]).groups()
adjuntos = re.compile('https://www\.hispachan\.org/%s/src/[0-9]+\.[^\'"]+' % tablon)
peticion = requests.get("https://www.hispachan.org/%s/res/%s.html" % (tablon, idpost))
# Si el hilo aun existe extrae los archivos
if peticion.status_code == 200:
    os.makedirs(os.path.join(tablon, idpost))
    for archivo in list(set(adjuntos.findall(peticion.content))):
        print "Descargando " + archivo
        descarga = requests.get(archivo)
        # El archivo basicamente se guarda en tablon/post/nombre
        salida = open(os.path.join(tablon, idpost, archivo.split("/")[-1]), "wb")
        salida.write(descarga.content)
        salida.close()
else: print("El hilo no existe")
