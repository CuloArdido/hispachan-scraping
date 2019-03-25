# -*- coding: utf-8 -*-
import sys
import os
import re
import threading
import queue
import time

import urllib.request
import urllib.error

URLError = urllib.error.URLError


# flags
subfolder = None
overwrite = None
update    = None

# shared stuff
nbitsmutx = threading.Lock()
nbits     = 0

# Expresiones regulares para evitar escribir codigo innecesariamente complejo
adjuntos = re.compile('<span class="file(?:namereply|size)">[\r\n]+<a[\s\r\n]+target="_blank"[\s\r\n]+href="([^"]+)"(?:[\s\S]*?)<span class="nombrefile"(?:>, ([^<]+)| title="([^"]+))')
enlace = re.compile("https?://(?:www\.)?hispachan\.org/([a-z]+)/res/([0-9]+)\.html")

def getthreadinfo(url):
    board, thread = enlace.match(url).groups()
    return (board, thread)


def getimglist(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0')
    ]
    try:
        f = opener.open(url, timeout=20)
        b = f.read()
    except URLError:
        raise
    f.close()

    return adjuntos.findall(b.decode('utf-8'))


def subprocess(iqueue, oqueue):
    while True:
        tmp = iqueue.get()
        if not tmp:
            break

        if saveimg(tmp[0], tmp[1]):
            oqueue.put((tmp[0], True))
            continue
        oqueue.put((tmp[0], False))


def saveimg(url, path):
    global nbits
    global nbitsmutx

    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0')
    ]
    try:
        f = opener.open(url, timeout=120)
    except URLError:
        return False
    except:
        return False

    if os.path.isfile(path):
        if update:
            try:
                sz1 = int(f.info()["Content-Length"])

                fh = open(path, "rb")
                fh.seek(0, 2)
                sz2 = fh.tell()
                fh.close()
            except:
                return False

            if sz1 == sz2:
                return True

        # si el archivo existe intentamos con un nuevo nombre
        if not update and not overwrite:
            fnme, fext = os.path.splitext(path)

            i = 1
            while os.path.isfile(path):
                path = fnme + "(" + str(i) +")" + fext
                i += 1

    try:
        fh = open(path, "wb")
        while True:
            b = f.read(4096)
            if not b:
                break

            nbitsmutx.acquire()
            nbits += len(b)
            nbitsmutx.release()

            fh.write(b)
        fh.close()
    except (IOError, URLError):
        return False
    except:
        return False
    return True


def saveimages(ilist, dpath):
    global nbits

    path = os.path.abspath(dpath)
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    print("Descargando {} imagenes en \n[{}]".format(len(ilist), path))

    iqueue = queue.Queue()
    oqueue = queue.Queue()

    threads = []
    for i in range(4):
        thr = threading.Thread(target=subprocess, args=(iqueue, oqueue))
        thr.daemon = True
        thr.start()
        threads.append(thr)

    for img in ilist:
        if not img[0]:
            continue

        link = img[0]
        name = img[1]
        if img[2]:
            name = img[2]
        iqueue.put((link, os.path.join(path, name)))

    f = 0
    i = 0
    try:
        while i < len(ilist):
            while not oqueue.empty():
                r = oqueue.get()
                
                print("\r..." + r[0][8:], end=" ")
                if not r[1]:
                    print("[FAILED]", end="")
                    f += 1
                print()
                i += 1

            print("\r{}Kb".format(nbits >> 10), end="")
            time.sleep(0.15)
    except KeyboardInterrupt:
        exit()

    print("\r{}Kb".format(nbits >> 10))
    print("Terminado: archivos descargados {}, errores {}".format(i - f, f))


usage = """
Uso: %s [opciones] <url del hilo o tablon/hilo> [<destino>]
Opciones:
    -no-subfolder     Omite la creacion de una subcarpeta para las imagenes.
    -overwrite        Sobrescribe los archivos con el mismo nombre.
    -update           Solo descarga los archivos que no existen.
""" % sys.argv[0]


def showusage():
    print(usage)
    exit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        showusage()
    sys.argv.pop(0)
    args = sys.argv

    # parametros
    options = {
        "-no-subfolder": ("subfolder",  True),
        "-overwrite":    ("overwrite", False),
        "-update":       ("update",    False)
    }

    s = globals()
    for option in options:
        m = options[option]
        s[m[0]] = m[1]

    while args[0] in options:
        a = args.pop(0)
        if not options[a]:  # parametro duplicado
            showusage()
        s[options[a][0]] = not options[a][1]
        options[a] = None

    if not args or len(args) > 2:
        showusage()

    r = getthreadinfo(args.pop(0))
    if not r:
        print("Error: url invalida")

    url = "https://hispachan.org/{}/res/{}.html".format(r[0], r[1])
    try:
        ilist = getimglist(url)
        if not ilist:
            print("Error: ningun archivo para descargar")
            exit()

        dpath = os.getcwd()
        if args:
            dpath = args[0]
        #
        if subfolder:
            dpath = os.path.join(dpath, r[0], r[1])
            saveimages(ilist, dpath)
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print("Error:", e)
