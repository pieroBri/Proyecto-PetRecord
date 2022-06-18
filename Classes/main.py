#Establecer conexion a servidor y base de datos en el inicio
#Validar token, validar llave y activar token
import os
import os.path
import uuid
import mysql.connector


db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()
mycursor.execute('select * from fichaMedica')

resultado = mycursor.fetchone()
print(resultado)

if (os.path.exists("infoTerminal.txt")):
    with open("infoTerminal.txt", "r") as f:
        lineasTexto = f.readlines()
        for i in lineasTexto:
            print(i)
else:
    with open("infoTerminal.txt", "w") as f: #si no existe el archivo lo creamos y le damos el formato default
        idRand = uuid.uuid4()
        print(idRand)
        f.write(f"id = {idRand}")


os.system("attrib +h infoTerminal.txt")