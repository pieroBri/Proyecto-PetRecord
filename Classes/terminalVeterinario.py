#ESTA ES LA CLASE MAIN, IMPORTAR LAS DEMAS CLASES ACA
from tkinter import *
import os
import os.path
from unicodedata import name
import uuid


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

#import para el uso de la interfaz grafica de qt
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


#from terminalVeterinario import TerminalVeterinario
from tablaMedica import TablaMedica
from mascota import Mascota

class TerminalVeterinario(QMainWindow):

    def __init__(self, id : uuid, tokenActivacion, idVeterinaria :uuid, nombreVeterinaria):
        super().__init__()
        uic.loadUi("Proyecto-PetRecord\Complementos\GUIAPP_keyInsert.ui", self)
        self.botonConfirmarkey.clicked.connect(self.validarLlaveConServidor) #metodos de botones en el contrusctor
        self.id = id
        self.tokenActivacion = tokenActivacion
        self.idVeterinaria = idVeterinaria
        self.nombreVeterinaria = nombreVeterinaria
        self.mascotas = [Mascota]
       


    def validarConexionInternet(self):
        pass

    def validarLlaveConServidor(self):

        #uic.loadUi("Proyecto-PetRecord/Complementos/AbstracMedico.ui", self) 

        llaveEntrada = self.keyInput.text()##obtiene los datos ingresados de tiene que ponder en nombre de la clase 
        #toma los valores como string
        llaveBaseDeDatos = mycursor.execute(f'SELECT Llaves FROM keysactivacion WHERE Llaves = {llaveEntrada}')
        resultado = mycursor.fetchall()
        print(resultado)

        if(llaveEntrada == resultado[0][0]):
            print("coincidencia")

        ##esto es prueba local para ver como sacar los datos cambiar a con el servidor

    def activarTokenDeActivacion(self):
        pass

    def consultaBDTokenDeActivacion(self):
        pass

    def validarTokenDeActivacion(self):
        pass

    def ingresarMascotaAlSistema(self, mascotaNueva):
        self.mascotas.append(mascotaNueva)

    def verificarMascotaEnSistema(self, idMascota):
        for i in self.mascotas:
            if(i.id == idMascota):
                return True
        return False

    def llenarinfoBasicaMascota(self, ):
        pass
    
    def editarInfoBasicaMascota():
        pass

    def buscarFichaMedica():
        pass
    
    def crearFichaMedicaConsulta():
        pass

    def editarFichaMedicaConsulta():
        pass

    def GenerarConexiónServidor():
        pass

    def ObtenerDatosMascota():
        pass

    def generarIdTerminal(self):
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
              
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = TerminalVeterinario(12,"true","1","PetLife")#datos de prueba
    GUI.show()
    sys.exit(app.exec_())

