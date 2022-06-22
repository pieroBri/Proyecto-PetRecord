#ESTA ES LA CLASE MAIN, IMPORTAR LAS DEMAS CLASES ACA
from tkinter import *
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

    def __init__(self):
        super().__init__()
        uic.loadUi("Proyecto-PetRecord\Complementos\GUIAPP_keyInsert.ui", self)
        self.botonConfirmarkey.clicked.connect(self.validarLlaveConServidor) #metodos de botones en el constructor
        
        self.id = self.generarIdTerminal()
        self.tokenActivacion = self.validarTokenDeActivacion()
        self.idVeterinaria = None
        self.nombreVeterinaria =  None
        self.mascotas = [Mascota]
       


    def validarConexionInternet(self):
        pass
        
    def setIdVeterinaria(self, idVet):
        self.idVeterinaria = idVet

    def setNombreVeterinaria(self, nombreVet):
        self.nombreVeterinaria = nombreVet    
    
    def validarLlaveConServidor(self):

        #uic.loadUi("Proyecto-PetRecord/Complementos/AbstracMedico.ui", self) 

        llaveEntrada = self.keyInput.text()##obtiene los datos ingresados de tiene que ponder en nombre de la clase 
        #toma los valores como string
        mycursor.execute(f'SELECT Llaves FROM keysactivacion WHERE Llaves = {llaveEntrada}')
        resultado = mycursor.fetchone()
        
        if(llaveEntrada == resultado[0]):
            mycursor.execute(f'SELECT Veterinaria_idVeterinaria FROM keysactivacion WHERE Llaves = {llaveEntrada}')
            idVetActual = mycursor.fetchone()
            
            mycursor.execute(f'SELECT Veterinaria_nombreVeterinaria FROM keysactivacion WHERE Llaves = {llaveEntrada}')
            nombreVetActual = mycursor.fetchone()
            print("holas ")
            self.activarTokenDeActivacion(idVetActual[0], nombreVetActual[0])

    def activarTokenDeActivacion(self, idVet, nombreVet):
        self.tokenActivacion = True
        sql = 'INSERT INTO terminalveterinario (idTerminalVeterinario, tokenDeActivación, Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s,%s,%s,%s)'
        val = (str(self.id),self.tokenActivacion,idVet,nombreVet)
        mycursor.execute(sql, val)
        db.commit()
        self.setIdVeterinaria(idVet)
        self.setNombreVeterinaria(nombreVet)

    def validarTokenDeActivacion(self)->bool :
        
        sql = 'SELECT tokenDeActivación FROM terminalveterinario WHERE idTerminalVeterinario = (%s)'
        val = (self.id)
        mycursor.execute(sql, (val,))
        resultado = mycursor.fetchone()

        if(resultado[0] == 1):
            uic.loadUi("Proyecto-PetRecord/Complementos/buscarMascota.ui", self) 

    def ingresarMascotaAlSistema(self, mascotaNueva: list):
        self.mascotas.append(mascotaNueva)
        mycursor.execute('')

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
                return f.read()
                
        else:
            with open("infoTerminal.txt", "w") as f: #si no existe el archivo lo creamos y le damos el formato default
                idRand = uuid.uuid4()
                f.write(f"{idRand}")
                return idRand
              
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = TerminalVeterinario()#datos de prueba
    GUI.show()
    sys.exit(app.exec_())


# sql = "INSERT INTO veterinaria (idVeterinaria, nombreVeterinaria) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)
# db.commit()

# sql = "Delete from veterinaria where idVeterinaria=%s"
# val = ("John",)
# mycursor.execute(sql, val)
# db.commit()

# sql = "UPDATE veterinaria set nombreVeterinaria=%s where idVeterinaria=%s"
# val = ("LOCOPEPE", "John")
# mycursor.execute(sql, val)