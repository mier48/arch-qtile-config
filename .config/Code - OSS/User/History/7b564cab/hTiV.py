import os
import glob
import shutil

path = input("¿Que carpeta quieres ordenar?\r\n")

# "G:\Downloads"
os.chdir(path)

if os.path.exists("documents"):
    pass
else:
    os.mkdir("documents")

if os.path.exists("zip"):
    pass
else:
    os.mkdir("zip")

if os.path.exists("iso"):
    pass
else:
    os.mkdir("iso")

if os.path.exists("exe"):
    pass
else:
    os.mkdir("exe")

if os.path.exists("bat"):
    pass
else:
    os.mkdir("bat")

if os.path.exists("images"):
    pass
else:
    os.mkdir("images")

if os.path.exists("videos"):
    pass
else:
    os.mkdir("videos")

if os.path.exists("varios"):
    pass
else:
    os.mkdir("varios")

doc = glob.glob("*.doc")
docx = glob.glob("*.docx")
pdf = glob.glob("*.pdf")
txt = glob.glob("*.txt")
rtf = glob.glob("*.rtf")
html = glob.glob("*.html")
htm = glob.glob("*.htm")
jpg = glob.glob("*.jpg")
png = glob.glob("*.png")
bat = glob.glob("*.bat")
exe = glob.glob("*.exe")
iso = glob.glob("*.iso")
zip = glob.glob("*.zip")
epub = glob.glob("*.epub")
img = glob.glob("*.img")
jpeg = glob.glob("*.jpeg")
ltc = glob.glob("*.ltc")
mp4 = glob.glob("*.mp4")
arw = glob.glob("*.arw")
rar = glob.glob("*.rar")
msi = glob.glob("*.msi")

#videos
for i in (mp4):
    shutil.move(i, 'videos')

#documents
for i in (doc):
    shutil.move(i, 'documents')

for i in (docx):
    shutil.move(i, 'documents')

for i in (pdf):
    shutil.move(i, 'documents')

for i in (txt):
    shutil.move(i, 'documents')

for i in (rtf):
    shutil.move(i, 'documents')

for i in (html):
    shutil.move(i, 'documents')

for i in (htm):
    shutil.move(i, 'documents')

for i in (epub):
    shutil.move(i, 'documents')

#images
for i in (png):
    shutil.move(i, 'images')

for i in (jpg):
    shutil.move(i, 'images')

for i in (jpeg):
    shutil.move(i, 'images')

for i in (arw):
    shutil.move(i, 'images')

#others
for i in (bat):
    shutil.move(i, 'bat')

for i in (exe):
    shutil.move(i, 'exe')

for i in (iso):
    shutil.move(i, 'iso')

for i in (img):
    shutil.move(i, 'iso')

for i in (zip):
    shutil.move(i, 'zip')

for i in (rar):
    shutil.move(i, 'zip')

for i in (msi):
    shutil.move(i, 'exe')


#varios
for i in (ltc):
    shutil.move(i, 'varios')
