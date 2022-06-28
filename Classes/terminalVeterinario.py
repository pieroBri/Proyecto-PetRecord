#ESTA ES LA CLASE MAIN, IMPORTAR LAS DEMAS CLASES ACA
from tkinter import *
import os
import os.path
import uuid


import mysql.connector

from fichaMedica import FichaMedica


db = mysql.connector.connect(
    user='piero',
    password='pieron123',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor(buffered = True)
mycursor.execute('select * from fichaMedica')


resultado = mycursor.fetchone()

#import para el uso de la interfaz grafica de qt
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *


#from terminalVeterinario import TerminalVeterinario
from tablaMedica import TablaMedica
from mascota import Mascota

class TerminalVeterinario(QMainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi("Complementos\GUIAPP_keyInsert.ui", self)
        # self.botonConfirmarkey.clicked.connect(self.validarLlaveConServidor) #metodos de botones en el constructor
        
        self.id = self.generarIdTerminal()
        self.tokenActivacion = None
        self.mascotas = []
        self.validarTokenDeActivacion()
        self.nombreVeterinaria = None
        self.idVeterinaria = None
        if (self.tokenActivacion == True):
            self.setIdVeterinaria()
            self.setNombreVeterinaria()
            self.setMascotas()
            
            
        

    def validarConexionInternet(self):
        pass
        
    def setIdVeterinaria(self):
        sql = 'SELECT Veterinaria_idVeterinaria FROM TerminalVeterinario WHERE idTerminalVeterinario = (%s)'
        mycursor.execute(sql, (str(self.id),))
        idVet = mycursor.fetchone()
        self.idVeterinaria = idVet[0]

    def setNombreVeterinaria(self):
        sql = 'SELECT Veterinaria_nombreVeterinaria FROM TerminalVeterinario WHERE idTerminalVeterinario = (%s)'
        mycursor.execute(sql, (str(self.id),))
        nombreVet = mycursor.fetchone()
        self.nombreVeterinaria = nombreVet[0]    
    
    def setMascotas(self):
        sql = 'SELECT Mascota_idMascota FROM Mascota_has_TerminalVeterinario WHERE TerminalVeterinario_Veterinaria_idVeterinaria = (%s)'
        mycursor.execute(sql, (str(self.idVeterinaria),))
        ids = mycursor.fetchall()
        for i in range(len(ids)):
            sql = 'SELECT * FROM Mascota WHERE idMascota = (%s)'
            mycursor.execute(sql, (str(ids[i][0]),))
            resultado = mycursor.fetchone()
            sql = 'SELECT * FROM RegistroDeOperaciones WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultado[9]),))
            registroOp = mycursor.fetchall()
            sql = 'SELECT * FROM RegistroVacunasSuministradas WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultado[9]),))
            registroVac = mycursor.fetchall()
            sql = 'SELECT * FROM Alergias WHERE TablaMedica_idTablaMedica = (%s)'
            mycursor.execute(sql, (str(resultado[9]),))
            alergiasEntregar = mycursor.fetchall()
            tablaEntregar = TablaMedica(resultado[9],  alergiasEntregar, registroOp, registroVac)
            mascotalol= Mascota(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5], resultado[6],
                                    resultado[7], resultado[8], tablaEntregar)
            mascotalol.getTablaMedica().cargarFichas()
            self.mascotas.append(mascotalol)
            
            
    def validarLlaveConServidor(self):

        #uic.loadUi("Proyecto-PetRecord/Complementos/AbstracMedico.ui", self) 

        llaveEntrada = self.keyInput.text()##obtiene los datos ingresados de tiene que ponder en nombre de la clase 
        #toma los valores como string
        mycursor.execute(f'SELECT Llaves FROM keysactivación WHERE Llaves = {llaveEntrada}')
        resultado = mycursor.fetchone()
        
        if(resultado == None):
            self.label_3.setVisible(True)
            self.validarLlaveConServidor()
        else:
            mycursor.execute(f'SELECT Veterinaria_idVeterinaria FROM Keysactivación WHERE Llaves = {llaveEntrada}')
            idVetActual = mycursor.fetchone()
            
            mycursor.execute(f'SELECT Veterinaria_nombreVeterinaria FROM Keysactivación WHERE Llaves = {llaveEntrada}')
            nombreVetActual = mycursor.fetchone()
            self.activarTokenDeActivacion(idVetActual[0], nombreVetActual[0])

    def activarTokenDeActivacion(self, idVet, nombreVet):
        self.tokenActivacion = True
        sql = 'INSERT INTO terminalveterinario (idTerminalVeterinario, tokenDeActivación, Veterinaria_idVeterinaria, Veterinaria_nombreVeterinaria) VALUES (%s,%s,%s,%s)'
        val = (str(self.id),self.tokenActivacion,idVet,nombreVet)
        mycursor.execute(sql, val)
        db.commit()
        self.setIdVeterinaria(idVet)
        self.setNombreVeterinaria(nombreVet)
        uic.loadUi("Complementos/buscarMascota.ui",self)

    def validarTokenDeActivacion(self):
        
        sql = 'SELECT tokenDeActivación FROM terminalveterinario WHERE idTerminalVeterinario = (%s)'
        val = (self.id)
        mycursor.execute(sql, (val,))
        resultado = mycursor.fetchone()
        
        if(resultado == None):
            uic.loadUi("Complementos/GUIAPP_KeyInsert.ui",self)
            self.botonConfirmarkey.clicked.connect(self.validarLlaveConServidor)
        elif(resultado[0] == 1):
            self.tokenActivacion = True
            uic.loadUi("Complementos/buscarMascota.ui", self)
            self.BotonBuscar.clicked.connect(self.verificarMascotaEnSistema)
            

    def ingresarMascotaAlSistema(self, mascotaNueva: list):
        self.mascotas.append(mascotaNueva)
        mycursor.execute('')

    def verificarMascotaEnSistema(self):
        idMascotaBuscada = self.inputBuscar.text()
        sql = 'SELECT idMascota FROM mascota WHERE idMascota = (%s)'
        mycursor.execute(sql, (idMascotaBuscada,))
        resultado = mycursor.fetchone()
        if(resultado != None):
            sql = 'SELECT Mascota_idMascota FROM Mascota_has_TerminalVeterinario WHERE TerminalVeterinario_Veterinaria_idVeterinaria = (%s)'
            mycursor.execute(sql, (self.idVeterinaria,))
            resultado = mycursor.fetchall()
            flagMascotaEnc = False
            for id in resultado:
                if(id[0] == str(idMascotaBuscada)):
                    flagMascotaEnc = True
            self.botonAgregar.setVisible(False)
            if(flagMascotaEnc):
                sql = 'SELECT * FROM mascota WHERE idMascota = (%s)'
                mycursor.execute(sql, (idMascotaBuscada,))
                resultado2 = mycursor.fetchone()
                self.datosMostrar.setText('Codigo mascota: ' + str(resultado2[0]) + ', Nombre mascota: ' 
                + str(resultado2[1]) + ', Especie: ' + str(resultado2[2]) + ', Raza: ' + str(resultado2[4]) + ', Dueño/a: ' + str(resultado2[5]))
                self.datosMostrar.setVisible(True)
                self.botonEntrar.setVisible(True)
                self.botonAbstracto.setVisible(False)
                for mascota in self.mascotas:
                    if(mascota.id == idMascotaBuscada):
                        mascotaMostrada = mascota
                self.botonEntrar.clicked.connect(lambda : self.verScreenDatosTotal(mascotaMostrada))
            else:
                sql = 'SELECT * FROM mascota WHERE idMascota = (%s)'
                mycursor.execute(sql, (idMascotaBuscada,))
                resultado2 = mycursor.fetchone()
                self.datosMostrar.setText('Codigo mascota: ' + str(resultado2[0]) + ', Nombre mascota: ' 
                + str(resultado2[1]) + ', Especie: ' + str(resultado2[2]) + ', Raza: ' + str(resultado2[4]) + ', Dueño/a: ' + str(resultado2[5]))
                self.datosMostrar.setVisible(True)
                self.botonAbstracto.setVisible(True)
                self.botonEntrar.setVisible(False)
        else:
            #Funcion registrar mascota
            self.datosMostrar.setText('Mascota no ingresada en el sistema')
            self.botonAgregar.setVisible(True)
            self.datosMostrar.setVisible(True)
            self.botonAbstracto.setVisible(False)
            self.botonEntrar.setVisible(False)
            self.llenarInfoBasicaMascota(idMascotaBuscada)

    def verScreenDatosTotal(self, mascotaMostrada:Mascota):
        alergias = ''
        operaciones = ''
        vacunas = ''
        uic.loadUi("Complementos/VistaDatosMascotaTotal.ui", self)
        value = self.infoBasicaMascota.item(0)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getNombreMascota()))
        value = self.infoBasicaMascota.item(1)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getEspecie()))
        value = self.infoBasicaMascota.item(2)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getRaza()))
        value = self.infoBasicaMascota.item(3)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getColorMascota()))
        value = self.infoBasicaMascota.item(4)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getRutTutor()))
        value = self.infoBasicaMascota.item(5)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getNumeroTelefono()))
        value = self.infoBasicaMascota.item(6)
        value.setText(value.text() + '  '+ str(mascotaMostrada.getDireccion()))

        tablaMedicaActual = mascotaMostrada.getTablaMedica()
        value2 = self.datoTablaMedica.item(0)
        for i in range(len(tablaMedicaActual.getAlergias())):
            alergias = alergias + str(tablaMedicaActual.getAlergias()[i][1])
        value2.setText(value2.text() + '  ' + alergias)
        
        value2 = self.datoTablaMedica.item(1)
        for i in range(len(tablaMedicaActual.getRegistroDeOperaciones())):
            operaciones = operaciones + str(tablaMedicaActual.getRegistroDeOperaciones()[i][1])
        value2.setText(value2.text() + '  ' + operaciones)

        value2 = self.datoTablaMedica.item(2)
        for i in range(len(tablaMedicaActual.getVacunasSuministradas())):
            vacunas = vacunas + str(tablaMedicaActual.getVacunasSuministradas()[i][1])
        value2.setText(value2.text() + '  ' + vacunas)

        for i in range(len(tablaMedicaActual.fichas)):
            item = QListWidgetItem('Ficha del : '+str(tablaMedicaActual.getFichas()[i].getFechaConsulta()))
            self.listWidFichas.addItem(item)

        self.botonFichaSelected.clicked.connect(lambda: self.getFichaMascota(mascotaMostrada))

    def getFichaMascota(self, mascotaMostrar:Mascota):
        itemSelected = self.listWidFichas.currentItem()
        cadenaAux = str(itemSelected.text())
        fecha = cadenaAux.split('Ficha del : ')
        fecha = fecha[1]
        fichas = mascotaMostrar.getTablaMedica().getFichas()

        for i in fichas:
            if (str(i.getFechaConsulta()) ==  str(fecha)):
                ficha = i
        
        self.verFichaMedica(ficha)
        


    def verFichaMedica(self,fichaMedica:FichaMedica):
        uic.loadUi("Complementos/formularioFicha.ui", self)
        print(str(fichaMedica.getFechaConsulta()))

        
    def llenarInfoBasicaMascota(self, idMascota):
        # self.ingresarMascotaAlSistema(mascotaEnviada)
        pass
    
    def editarInfoBasicaMascota(self, idMascota):
        for mascota in self.mascotas:
            if(idMascota == mascota):
                mascota.editarInfoBasicaMascota()
        pass

    def buscarFichaMedica(self, idMascota):
        for mascota in self.mascotas:
            if(idMascota == mascota):
                mascota.buscarFichaMedica()
        pass
    
    def crearFichaMedicaConsulta(self, idMascota):
        for mascota in self.mascotas:
            if(idMascota == mascota):
                mascota.crearFichaMedicaConsulta()
        pass

    def editarFichaMedicaConsulta(self, idMascota):
        for mascota in self.mascotas:
            if(idMascota == mascota):
                mascota.editarFichaMedicaConsulta()
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