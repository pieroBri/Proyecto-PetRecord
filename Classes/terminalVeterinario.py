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
from PyQt5 import uic, QtCore
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
             # De ser el caso que el token esta ya activado, se instancian aquí, debido a que actToken no se llamará
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
        # Se setean los atributos de la clase cuando se activa el token
        self.setIdVeterinaria()
        self.setNombreVeterinaria()
        self.setMascotas()
        uic.loadUi("Complementos/buscarMascota.ui",self)
        self.BotonBuscar.clicked.connect(self.verificarMascotaEnSistema)

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
                    if(mascota.getId() == idMascotaBuscada):
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
        self.agregarFicha.clicked.connect(lambda: self.crearFichaMedicaConsulta(mascotaMostrada))


    def getFichaMascota(self, mascotaMostrar:Mascota):
        itemSelected = self.listWidFichas.currentItem()
        cadenaAux = str(itemSelected.text())
        fecha = cadenaAux.split('Ficha del : ')
        fecha = fecha[1]
        fichas = mascotaMostrar.getTablaMedica().getFichas()

        for i in fichas:
            if (str(i.getFechaConsulta()) ==  str(fecha)):
                ficha = i
        
        self.verFichaMedica(ficha, mascotaMostrar)
        

    def verFichaMedica(self,fichaMedica:FichaMedica, mascotaVolver):
        uic.loadUi("Complementos/formularioFicha.ui", self)

        if not fichaMedica.getOperacion():
            self.botonAgregarFichaOperacion.setVisible(False)

        if not fichaMedica.getHospitalizacion():
            self.botonAgregarFichaHosp.setVisible(False)

        if not fichaMedica.getSedacion():
            self.botonAgregarFichaSedacion.setVisible(False)
            

        self.buttAgregarTratamientos.setVisible(False)
        self.buttAgregarMedicamentos.setVisible(False)
        self.buttAgregarVacunas.setVisible(False)
        self.botonAgregarFicha.setVisible(False)

        boton = QPushButton(self.contenedorBoton)
        boton.setText('Volver')
        boton.setGeometry(0,0,131,51)
        boton.clicked.connect(lambda : self.verScreenDatosTotal(mascotaVolver))
        
        dateAux = str(fichaMedica.getFechaConsulta())
        date = dateAux.split(' ')
        date = date[0]
        qdate = QtCore.QDate.fromString(date, "yyyy-MM-dd")

        self.fechaConsulta.setDisplayFormat("yyyy-MM-dd")

        self.inputSucursal.setText(str(fichaMedica.getSucursalVeterinaria()))
        self.inputSucursal.setReadOnly(True)
        self.inputVetCargo.setText(str(fichaMedica.getVeterinarioACargo()))
        self.inputVetCargo.setReadOnly(True)
        self.fechaConsulta.setDate(qdate)
        
        self.inputFrecRespiratoria.setText(str(fichaMedica.getFrecRespiratoria()))
        self.inputFrecRespiratoria.setReadOnly(True)
        self.inputFrecCardiaca.setText(str(fichaMedica.getFrecCardiaca()))
        self.inputFrecRespiratoria.setReadOnly(True)
        self.inputPeso.setText(str(fichaMedica.getPeso()))
        self.inputEdad.setText(str(fichaMedica.getEdad()))
        self.inputEdad.setReadOnly(True)
        self.inputTemp.setText(str(fichaMedica.getTemp()))
        self.inputTemp.setReadOnly(True)
        
        tratamientos = fichaMedica.getTratamiento()
        medicamentos = fichaMedica.getMedicamentosConsulta()
        vacunas = fichaMedica.getVacunasSuministradasConsulta()

        for tratamiento in tratamientos:
            item = QListWidgetItem(str(tratamiento["nombreTratamiento"]))
            self.inputCausaVisita.setText(str(tratamiento['causaVisita']))
            self.tratamientosList.addItem(item)

        for medicamento in medicamentos:
            item = QListWidgetItem(str(medicamento["nomMedicamento"]))
            self.medicamentosList.addItem(item)

        for vacuna in vacunas:
            item = QListWidgetItem(str(vacuna["nomVacuna"]))
            self.vacunasList.addItem(item)

        
    def llenarInfoBasicaMascota(self, idMascotaBuscada):

        # self.ingresarMascotaAlSistema(mascotaEnviada)
        pass
    
    def editarInfoBasicaMascota(self, idMascota):
        for mascota in self.mascotas:
            if(idMascota == mascota):
                mascota.editarInfoBasicaMascota()
        pass

    def buscarFichaMedica(self, idMascota):
        for mascota in self.mascotas:
            if(idMascota == mascota.getId()):
                mascota.buscarFichaMedica()
        pass
    
    def crearFichaMedicaConsulta(self, mascota : Mascota):

        uic.loadUi("Complementos/formularioCrearFicha.ui", self)

        # Generar id ficha
        # idFicha = uuid.uuid4()
        # idTabla = mascota.getTablaMedica().getId()
        # sucursalVet = self.inputSucursal.text()
        # vetACargo = self.inputVetCargo.text()
        # date = self.fechaConsulta.date()
        # date = date.toPyDate()
        # frecResp = self.inputFrecRespiratoria.text()
        # frecCard = self.inputFrecCardiaca.text()
        # peso = self.inputPeso.text()
        # edad = self.inputEdad.text()
        # temp = self.inputTemp.text()
        
        # causaVisita = self.inputCausaVisita.text()
        # tratamientosAux = self.inputTratamientos.text()
        # medicamentosAux = self.inputMedicamentos.text()
        # vacunasAux = self.inputVacunas.text()
        # print(str(idTabla) + str())
        # tratamientosAux = tratamientosAux.split(';')
        # operacion = []
        # hospt = []
        # sedacion = []
        # operacion.append(False)
        # hospt.append(False)
        # sedacion.append(False)
        # self.botonAgregarFichaOperacion.clicked.connect(lambda : self.crearFichaOperacion(mascota, operacion))
        # self.botonAgregarFichaHosp.clicked.connect(lambda : self.crearFichaHospitalizacion(mascota, hospt))
        # self.botonAgregarFichaSedacion.clicked.connect(lambda : self.crearFichaSedacion(mascota, sedacion))
          

        self.botonAgregarFicha.clicked.connect(lambda : self.guardarFichaBd(mascota))
        


    def guardarFichaBd(self, mascota):

        idFicha = uuid.uuid4()
        idTabla = mascota.getTablaMedica().getId()
        sucursalVet = self.inputSucursal.text()
        vetACargo = self.inputVetCargo.text()
        date = self.fechaConsulta.date()
        date = date.toPyDate()
        frecResp = self.inputFrecRespiratoria.text()
        frecCard = self.inputFrecCardiaca.text()
        peso = self.inputPeso.text()
        edad = self.inputEdad.text()
        temp = self.inputTemp.text()
        
        causaVisita = self.inputCausaVisita.text()
        tratamientosAux = self.inputTratamientos.text()
        medicamentosAux = self.inputMedicamentos.text()
        vacunasAux = self.inputVacunas.text()
        print('------------'+str(date))
        tratamientosAux = tratamientosAux.split(';')
        operacion = []
        hospt = []
        sedacion = []
        operacion.append(False)
        hospt.append(False)
        sedacion.append(False)
        self.botonAgregarFichaOperacion.clicked.connect(lambda : self.crearFichaOperacion(mascota, operacion[0]))
        self.botonAgregarFichaHosp.clicked.connect(lambda : self.crearFichaHospitalizacion(mascota, hospt[0]))
        self.botonAgregarFichaSedacion.clicked.connect(lambda : self.crearFichaSedacion(mascota, sedacion[0]))

        ficham = FichaMedica(idFicha, sucursalVet, vetACargo, date, operacion[0], frecResp, frecCard, peso, edad, hospt[0], sedacion[0], temp, idTabla)

        ficham.setVacFicha()
        ficham.setMedicamentosConsulta()
        ficham.setTratamiento()
        mascota.getTablaMedica().getFichas().append(ficham)

        sql = 'INSERT INTO FichaMedica VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(sql, (str(ficham.getId()), str(ficham.getSucursalVeterinaria()), str(ficham.getVeterinarioACargo()), str(ficham.getFechaConsulta()), ficham.getOperacion(), str(ficham.getFrecRespiratoria()), str(ficham.getFrecCardiaca()), ficham.getPeso(), str(ficham.getEdad()), ficham.getHospitalizacion(), ficham.getSedacion(), ficham.getTemp(), str(ficham.getIdTabla())))
        db.commit()
        tratamientos = []
        for trat in tratamientosAux:
            tratamientos.append(trat)
            idTratamiento = str(uuid.uuid4())
            sql = 'INSERT INTO TratamientosConsulta (idTratamientosConsulta, nombreTratamientos, caudaDeLaVisita, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s, %s)'
            mycursor.execute(sql, (str(idTratamiento), str(trat), str(causaVisita), str(ficham.getId()), str(ficham.getIdTabla())))
            db.commit()
        
        
        medicamentos = []
        medicamentosAux = medicamentosAux.split(';')
        for med in medicamentosAux:
            medicamentos.append(med)
            idMedicamento = str(uuid.uuid4())
            sql = 'INSERT INTO MedicamentosConsulta (idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (str(idMedicamento), str(med), str(ficham.getId()), str(ficham.getIdTabla())))
            db.commit()
        
        vacunas = []
        vacunasAux = vacunasAux.split(';')
        for vac in vacunasAux:
            vacunas.append(vac)
            idVacunas = str(uuid.uuid4())
            sql = 'INSERT INTO VacunasSuministradasConsulta (idVacunasSuministradas, nombreVacuna, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (str(idVacunas), str(vac), str(ficham.getId()), str(ficham.getIdTabla())))
            db.commit()
        
        # (idFichaMedica, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecuenciaRespiratoria, frecuenciaCardiaca, peso, edad, hospitalizacion, sedacion, temperatura, TablaMedica_idTablaMedica)
        


    def crearFichaOperacion(self, mascota, operacion):
        operacion[0] = True
        uic.loadUi("Complementos/formularioFichaAuthCirugia.ui", self)

        pass

    def crearFichaHospitalizacion(self, mascota, hospt):
        hospt[0] = True
        uic.loadUi("Complementos/formularioFichaHospitalizacion.ui", self)
        pass

    def crearFichaSedacion(self, mascota, sedacion):
        sedacion[0] = True
        uic.loadUi("Complementos/formularioFichaSedacion.ui", self)
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
                return str(idRand)


              
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