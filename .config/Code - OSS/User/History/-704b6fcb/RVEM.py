from cryptography.fernet import Fernet
import base64, hashlib
import os, sys
# from os import listdir
# from os.path import isfile, join
from os import walk

def encrypt(key, filename):
	outFile = os.path.join(os.path.dirname(filename), "__(encrypted)__" + os.path.basename(filename))
	
	encryptor = Fernet(key)
	
	with open(filename, "rb") as infile:
		with open(outFile, "wb") as outfile:
			data = infile.read()
			outfile.write(encryptor.encrypt(data))

def decrypt(key, filename):
	outFile = os.path.join(os.path.dirname(filename), os.path.basename.replace("__(encrypted)__", ""))
	decryptor = Fernet(key)

	with open(filename, "rb") as infile:
		with open(outFile, "wb") as outfile:
			data = infile.read()
			outfile.write(decryptor.decrypt(data))

def display_info():
	print('\r\n¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦')
	print('¦', '		 Creado por: Alberto Mier	               ' , '¦')
	print('¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦')

def allfiles():
	allFiles = []
	for (dirpath, dirnames, filenames) in walk("CryptoFile/DATA"):
		for file in filenames:
			allFiles.append(os.path.join(dirpath, file))

	return allFiles
	
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

display_info()
choice = input("¿Quieres (E)ncriptar o (D)esencriptar?")
#password = input("Enter the password: ")
my_password = 'mypassword'.encode()
key = hashlib.md5(my_password).hexdigest()
key_64 = base64.urlsafe_b64encode(key.encode("utf-8"))

encFiles = allfiles()

if choice == "E":
	a = 0
	l = len(encFiles)
	if l == 0 :
		print("No hay archivos para encriptar")
	else:		
		print(f"Encriptando {l} archivos")
		printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
		for Tfiles in encFiles:	
			if os.path.basename(Tfiles).startswith("__(encrypted)__"):
				pass

			elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
				pass 
			else:
				encrypt(key_64, str(Tfiles))
				os.remove(Tfiles)

			a = a+1
			printProgressBar(a, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


elif choice == "D":
	a = 0
	print(f"Desencriptando archivos")
	l = len(encFiles)
	printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	for Tfiles in encFiles:
		if os.path.basename(Tfiles).startswith("__(encrypted)__"):
			decrypt(key_64, str(Tfiles))
			os.remove(Tfiles)
		a = a+1
		printProgressBar(a, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
