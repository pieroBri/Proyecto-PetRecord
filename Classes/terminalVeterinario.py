#ESTA ES LA CLASE MAIN, IMPORTAR LAS DEMAS CLASES ACA
from ast import Str
from tkinter import *
import os
import os.path
import uuid

from datetime import datetime
from webbrowser import get
import mysql.connector
import socket

from fichaMedica import FichaMedica

db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor(buffered = True)
mycursor.execute('select * from fichaMedica')


resultado = mycursor.fetchone()

#import para el uso de la interfaz grafica de qt
import sys
from PyQt5 import uic, QtCore, QtGui
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
        try:
            socket.create_connection(('Google.com',80))
            return True
        except OSError:
            return False
        
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
        self.consultaBDtokenDeActivacion()
        self.cargarScreenBuscarMascota() #se carga la screen buscarMascota

    def consultaBDtokenDeActivacion(self):
        self.setIdVeterinaria()
        self.setNombreVeterinaria()
        self.setMascotas()

    def validarTokenDeActivacion(self):
        
        if(self.validarConexionInternet()): #pimero valida la conexión si hay pasa
            print("si hay conexion")
            sql = 'SELECT tokenDeActivación FROM terminalveterinario WHERE idTerminalVeterinario = (%s)'
            val = (self.id)
            mycursor.execute(sql, (val,))
            resultado = mycursor.fetchone()
            
            if(resultado == None):
                self.cargarScreenLlave()
            elif(resultado[0] == 1):
                self.tokenActivacion = True
                self.cargarScreenBuscarMascota() 
                
        else:
            print("no hay conexion a internet") 
            #hacer una screen de volver aconectar   

    def cargarScreenLlave(self):
        uic.loadUi("Complementos/GUIAPP_KeyInsert.ui",self)
        self.botonConfirmarkey.clicked.connect(self.validarLlaveConServidor)

    def cargarScreenBuscarMascota(self):
        uic.loadUi("Complementos/buscarMascota.ui", self)
        self.MensajeErrorBusqueda.setVisible(False)
        self.BotonBuscar.clicked.connect(self.verificarMascotaEnSistema)
    
    def ingresarMascotaAlSistema(self, mascotaNueva: Mascota):
        self.mascotas.append(mascotaNueva)
        sql = "INSERT INTO mascota (idMascota, nombreMascota, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, Dirección, TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, (str(mascotaNueva.getId()), str(mascotaNueva.getNombreMascota()) ))
        mycursor.execute('')
    
    def buscarMascotaLocal(self, idMascotaBuscada):
        # sql = 'SELECT * FROM mascota WHERE idMascota = (%s)'
        # mycursor.execute(sql, (idMascotaBuscada,))
        # resultado2 = mycursor.fetchone()
        for mascota in self.mascotas:
            if(mascota.getId() == idMascotaBuscada):
                mascotaMostrada = mascota
                self.datosMostrar.setText('Codigo mascota: ' + str(mascota.getId()) + ', Nombre mascota: '
                + str(mascota.getNombreMascota()) + ', Especie: ' + str(mascota.getEspecie() + ', Raza: ' + str(mascota.getRaza()) + ', Dueño/a: ' + str(mascota.getNombreTutor())))
        self.datosMostrar.setVisible(True)
        self.botonEntrar.setVisible(True)
        self.botonAbstracto.setVisible(False)
        
        self.botonEntrar.clicked.connect(lambda : self.verScreenDatosTotal(mascotaMostrada))
    
    def BuscarMascota(self, idMascotaBuscada):
        sql = 'SELECT * FROM mascota WHERE idMascota = (%s)' #muestra informacion bascia buscar 
        mycursor.execute(sql, (idMascotaBuscada,))
        resultado2 = mycursor.fetchone()
        self.datosMostrar.setText('Codigo mascota: ' + str(resultado2[0]) + ', Nombre mascota: ' 
        + str(resultado2[1]) + ', Especie: ' + str(resultado2[2]) + ', Raza: ' + str(resultado2[4]) + ', Dueño/a: ' + str(resultado2[5]))
                
    def verificarMascotaEnSistema(self):

        if(self.inputBuscar.text() != ""): #& len(self.inputBuscar.text()) == 15):
            self.MensajeErrorBusqueda.setVisible(False)
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
                    self. buscarMascotaLocal(idMascotaBuscada)
                else:
                    self.BuscarMascota(idMascotaBuscada)
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
                self.botonAgregar.clicked.connect(lambda : self.llenarInfoBasicaMascota(idMascotaBuscada))
        else:
            self.MensajeErrorBusqueda.setVisible(True)

    def verScreenDatosTotal(self, mascotaMostrada:Mascota):
        alergias = ''
        operaciones = ''
        vacunas = ''
        uic.loadUi("Complementos/VistaDatosMascotaTotal.ui", self)
        self.mensajeErrorSeleccionFicha.setVisible(False)
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


        self.botonVolver.clicked.connect(self.volverBuscar)
        self.botonFichaSelected.clicked.connect(lambda: self.getFichaMascota(mascotaMostrada))
        self.agregarFicha.clicked.connect(lambda: self.crearFichaMedicaConsulta(mascotaMostrada))

    def volverBuscar(self):
        uic.loadUi("Complementos/buscarMascota.ui", self)
        self.verificarMascotaEnSistema()
        
        
    def getFichaMascota(self, mascotaMostrar:Mascota):
        itemSelected = self.listWidFichas.currentItem()
   
        if(itemSelected != None):
            self.mensajeErrorSeleccionFicha.setVisible(False)
            cadenaAux = str(itemSelected.text())
            fecha = cadenaAux.split('Ficha del : ')
            fecha = fecha[1]
            fichas = mascotaMostrar.getTablaMedica().getFichas()

            for i in fichas:
                if (str(i.getFechaConsulta()) ==  str(fecha)):
                    ficha = i
            
            self.verFichaMedica(ficha, mascotaMostrar)
        else:
            self.mensajeErrorSeleccionFicha.setVisible(True)
        

    def verFichaMedica(self, fichaMedica:FichaMedica, mascotaVolver):
        uic.loadUi("Complementos/formularioFicha.ui", self)

        if not fichaMedica.getOperacion():
            self.botonVerFichaOperacion.setVisible(False)
        else:
            self.botonVerFichaOperacion.clicked.connect(lambda: self.verFichaOp(fichaMedica, mascotaVolver))
        if not fichaMedica.getHospitalizacion():
            self.botonVerFichaHosp.setVisible(False)
        else:
            self.botonVerFichaHosp.clicked.connect(lambda: self.verFichaHosp(fichaMedica, mascotaVolver))
        if not fichaMedica.getSedacion():
            self.botonVerFichaSedacion.setVisible(False)
        else:
            self.botonVerFichaSedacion.clicked.connect(lambda: self.verFichaSedacion(fichaMedica, mascotaVolver))
            
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
        nombreMascota = self.inputNombreMascota.text()
        especie = self.inputEspecie.text()
        color = self.inputColor.text()
        raza = self.inputRaza.text()
        nomTutor = self.inputNombreTutor.text()
        rut = self.inputRutTutor.text()
        numero = self.inputNumTelefono.text()
        direccion = self.inputDireccion.text()
        #alergias = self.
        idTabla = str(uuid.uuid4())
        mascotaEnviada = Mascota(idMascotaBuscada, nombreMascota, especie, color, raza, nomTutor, rut, numero, direccion,)
        self.ingresarMascotaAlSistema(mascotaEnviada)
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
        self.botonAgregarFichaOperacion.setEnabled(False)
        self.botonAgregarFichaHosp.setEnabled(False)
        self.botonAgregarFichaSedacion.setEnabled(False)
        
        self.inputFrecRespiratoria.setPlaceholderText("35rpm")
        self.inputFrecRespiratoria.setFocus()
        self.inputFrecCardiaca.setPlaceholderText("35bpm")
        self.inputFrecCardiaca.setFocus()
        self.inputPeso.setPlaceholderText("Peso en kg 3.34")
        self.inputPeso.setFocus()
        self.inputEdad.setPlaceholderText("3 años o meses o dias")
        self.inputEdad.setFocus()
        self.inputTemp.setPlaceholderText("temperatura en grados 12.1")
        self.inputTemp.setFocus()
        self.inputTratamientos.setPlaceholderText("desparasitación; vacunación")
        self.inputTratamientos.setFocus()
        self.inputMedicamentos.setPlaceholderText("tetraciclina; tobramicina")
        self.inputMedicamentos.setFocus()
        self.inputVacunas.setPlaceholderText("distemper; parvovirus")
        self.inputVacunas.setFocus()
        
        self.botonAgregarFicha.clicked.connect(lambda : self.guardarFichaBd(mascota))

        self.botonVolver.clicked.connect(lambda : self.verScreenDatosTotal(mascota))
        


    def guardarFichaBd(self, mascota):
    
        idFicha = uuid.uuid4()
        idTabla = mascota.getTablaMedica().getId()
        # Obtener el texto de los campos de la screen
        sucursalVet = self.inputSucursal.text()
        vetACargo = self.inputVetCargo.text()
        date = self.fechaConsulta.date()
        date = date.toPyDate()
        frecResp = self.inputFrecRespiratoria.text()
        frecCard = self.inputFrecCardiaca.text()
        peso = self.inputPeso.text()
        edad = self.inputEdad.text()
        temp = self.inputTemp.text()
        # -------------
        
        hospt = False
        sedacion = False
        operacion = False
        
        causaVisita = self.inputCausaVisita.text()
        tratamientosAux = self.inputTratamientos.text()
        medicamentosAux = self.inputMedicamentos.text()
        vacunasAux = self.inputVacunas.text()
        uic.loadUi("Complementos/formularioCrearFicha.ui", self)
        self.botonAgregarFicha.setEnabled(False)
        self.botonVolver.clicked.connect(lambda : self.verScreenDatosTotal(mascota))
        validator = QtGui.QIntValidator(1,100, self)
        # SET texto de los campos de la screen
        self.inputSucursal.setText(sucursalVet)
        self.inputVetCargo.setText(vetACargo)
        qdate = QtCore.QDate.fromString(str(date), "yyyy-MM-dd")
        self.fechaConsulta.setDisplayFormat("yyyy-MM-dd")
        self.fechaConsulta.setDate(qdate)
        self.inputFrecRespiratoria.setText(str(frecResp))
        self.inputFrecCardiaca.setText(str(frecCard))
        self.inputPeso.setText(str(peso))
        self.inputPeso.setValidator(validator)
        self.inputEdad.setText(str(edad))
        self.inputTemp.setText(str(temp))
        self.inputCausaVisita.setText(causaVisita)
        self.inputTratamientos.setText(tratamientosAux)
        self.inputMedicamentos.setText(medicamentosAux)
        self.inputVacunas.setText(vacunasAux)
        # ------------------
        
        self.botonAgregarFichaOperacion.setEnabled(True)
        self.botonAgregarFichaHosp.setEnabled(True)
        self.botonAgregarFichaSedacion.setEnabled(True)
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        date = f'{date} {current_time}'
        ficham = FichaMedica(idFicha, sucursalVet, vetACargo, date, operacion, frecResp, frecCard, peso, edad, hospt, sedacion, temp, idTabla)
        
        sql = 'INSERT INTO FichaMedica VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        mycursor.execute(sql, (str(ficham.getId()), str(ficham.getSucursalVeterinaria()), str(ficham.getVeterinarioACargo()), str(ficham.getFechaConsulta()), ficham.getOperacion(), str(ficham.getFrecRespiratoria()), str(ficham.getFrecCardiaca()), ficham.getPeso(), str(ficham.getEdad()), ficham.getHospitalizacion(), ficham.getSedacion(), ficham.getTemp(), str(ficham.getIdTabla())))
        db.commit()
        tratamientosAux = tratamientosAux.split(';')
        medicamentosAux = medicamentosAux.split(';')
        vacunasAux = vacunasAux.split(';')
        tratamientos = []
        tratClase = []
        tratDicc = {}
        for trat in tratamientosAux:
            tratamientos.append(trat)
            idTratamiento = str(uuid.uuid4())
            tratDicc = {
                'id' : idTratamiento,
                'nombreTratamiento': trat,
                'causaVisita' : causaVisita,
            }
            tratClase.append(tratDicc)
            sql = 'INSERT INTO TratamientosConsulta (idTratamientosConsulta, nombreTratamientos, caudaDeLaVisita, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s, %s)'
            mycursor.execute(sql, (str(idTratamiento), str(trat), str(causaVisita), str(ficham.getId()), str(ficham.getIdTabla())))
            db.commit()
        
        
        medicamentos = []
        medClase = []
        medDicc = {}
        
        for med in medicamentosAux:
            medicamentos.append(med)
            idMedicamento = str(uuid.uuid4())
            medDicc = {
                'id' : idMedicamento,
                'nomMedicamento' : med,
            }
            medClase.append(medDicc)
            sql = 'INSERT INTO MedicamentosConsulta (idMedicamentosConsulta, nombreMedicamentos, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (str(idMedicamento), str(med), str(ficham.getId()), str(ficham.getIdTabla())))
            db.commit()
        
        vacunas = []
        vacClase = []
        vacDicc = {}
        
        for vac in vacunasAux:
            vacunas.append(vac)
            idVacunas = str(uuid.uuid4())
            vacDicc = {
                'id' : idVacunas,
                'nomVacuna' : vac,
            }
            vacClase.append(vacDicc) 
            sql = 'INSERT INTO VacunasSuministradasConsulta (idVacunasSuministradas, nombreVacuna, FichaMedica_idFichaMedica, FichaMedica_TablaMedica_idTablaMedica) VALUES (%s, %s, %s, %s)'
            mycursor.execute(sql, (str(idVacunas), str(vac), str(ficham.getId()), str(ficham.getIdTabla())))
            db.commit()
        
    
        self.setearDatosLocal(ficham, tratClase, medClase, vacClase, mascota)
        self.botonAgregarFichaOperacion.clicked.connect(lambda: self.crearFichaOperacion(mascota, ficham))
        self.botonAgregarFichaHosp.clicked.connect(lambda: self.crearFichaHospitalizacion(mascota, ficham))
        self.botonAgregarFichaSedacion.clicked.connect(lambda: self.crearFichaSedacion(mascota, ficham))
     
    
    
    
    def setearDatosLocal(self, ficham, tratClase, medClase, vacClase, mascota):
        ficham.setTratamientoLocal(tratClase)
        ficham.setMedicamentosConsultaLocal(medClase)
        ficham.setVacFichaLocal(vacClase)

        mascota.getTablaMedica().getFichas().append(ficham)

    def crearFichaOperacion(self, mascota : Mascota, ficha : FichaMedica): # tratamientos, medicamentos, vacunas, causaVisita
        uic.loadUi("Complementos/formularioFichaAuthCirugia.ui", self)
        self.inputNombrePaciente.setText(mascota.getNombreMascota()) #se setean todos los valores ya obtenidos
        self.inputNombrePaciente.setReadOnly(True)
        self.inputPeso.setText(ficha.getPeso())
        self.inputPeso.setReadOnly(True)
        self.inputEspecie.setText(mascota.getEspecie())
        self.inputEspecie.setReadOnly(True)
        self.inputEdad.setText(ficha.getEdad())
        self.inputEdad.setReadOnly(True)
        self.inputRaza.setText(mascota.getRaza())
        self.inputRaza.setReadOnly(True)
        self.inputColor.setText(mascota.getColorMascota())
        self.inputColor.setReadOnly(True)
        self.inputNomTutor.setText(mascota.getNombreTutor())
        self.inputNomTutor.setReadOnly(True)
        self.inputRut.setText(mascota.getRutTutor())
        self.inputRut.setReadOnly(True)
        self.inputNumTelefono.setText(mascota.getNumeroTelefono())
        self.inputNumTelefono.setReadOnly(True)
        self.inputDireccion.setText(mascota.getDireccion())
        self.inputDireccion.setReadOnly(True)
        self.botonAgregarFCirugia.setEnabled(True)

        self.botonAgregarFCirugia.clicked.connect(lambda : self.agregarFichaOpBd(mascota, ficha))

    def agregarFichaOpBd(self, mascota :Mascota, ficha : FichaMedica):
        operacion = True
        autorizacion = self.checkAuth.isChecked()
        diagnostico = self.inputDiagnostico.toPlainText()
        cirugiaARealizar = self.inputCirugia.toPlainText()
        idOp = uuid.uuid4()
        
        sql = 'UPDATE fichaMedica SET operación=(%s) WHERE idFichaMedica = (%s)'
        mycursor.execute(sql, (operacion, str(ficha.getId())))
        db.commit()

        sql = 'INSERT INTO fichaOperación VALUES (%s, %s, %s, %s, %s, %s)'
        mycursor.execute(sql, (str(idOp), str(diagnostico), str(cirugiaARealizar), autorizacion, str(ficha.getId()), str(ficha.getIdTabla())))
        db.commit()

        ficha.setOperacion(operacion)
        opDicc = {}
        for ficham in mascota.getTablaMedica().getFichas():
            if(ficham.getId() == ficha.getId()):
                ficham.setOperacion(ficha.getOperacion)
                opDicc = {
                    'id':idOp,
                    'diagnostico':diagnostico,
                    'cirugiaARealizar':cirugiaARealizar,
                    'autTutor': autorizacion
                }
                ficham.setOpFichaLocal(opDicc)

        self.volverACrearFicha(mascota, ficha)

    def verFichaOp(self, ficha: FichaMedica, mascota: Mascota):
        uic.loadUi("Complementos/formularioFichaAuthCirugia.ui", self)
        self.inputNombrePaciente.setText(mascota.getNombreMascota()) #se setean todos los valores ya obtenidos
        self.inputNombrePaciente.setReadOnly(True)
        self.inputPeso.setText(str(ficha.getPeso()))
        self.inputPeso.setReadOnly(True)
        self.inputEspecie.setText(mascota.getEspecie())
        self.inputEspecie.setReadOnly(True)
        self.inputEdad.setText(ficha.getEdad())
        self.inputEdad.setReadOnly(True)
        self.inputRaza.setText(mascota.getRaza())
        self.inputRaza.setReadOnly(True)
        self.inputColor.setText(mascota.getColorMascota())
        self.inputColor.setReadOnly(True)
        self.inputNomTutor.setText(mascota.getNombreTutor())
        self.inputNomTutor.setReadOnly(True)
        self.inputRut.setText(mascota.getRutTutor())
        self.inputRut.setReadOnly(True)
        self.inputNumTelefono.setText(mascota.getNumeroTelefono())
        self.inputNumTelefono.setReadOnly(True)
        self.inputDireccion.setText(mascota.getDireccion())
        self.inputDireccion.setReadOnly(True)
        self.checkAuth.setChecked(True)
        self.checkAuth.setEnabled(False)
        self.botonAgregarFCirugia.setVisible(False)

        dicc = ficha.getOperacionFicha()

        self.inputDiagnostico.setPlainText(str(dicc["diagnostico"]))
        self.inputDiagnostico.setReadOnly(True)

        self.inputCirugia.setPlainText(str(dicc["cirugiaARealizar"]))
        self.inputCirugia.setReadOnly(True)

        boton = QPushButton(self.contenedorBotonOperacion)
        boton.setText('Volver')
        boton.setGeometry(0,0,131,51)
        boton.clicked.connect(lambda : self.verFichaMedica(ficha, mascota))
        
    def volverACrearFicha(self, mascota : Mascota, ficha : FichaMedica):
        uic.loadUi("Complementos/formularioCrearFicha.ui", self)

        self.inputSucursal.setText(ficha.getSucursalVeterinaria())
        self.inputSucursal.setReadOnly(True)
        self.inputVetCargo.setText(ficha.getVeterinarioACargo())
        self.inputVetCargo.setReadOnly(True)
        qdate = QtCore.QDate.fromString(str(ficha.getFechaConsulta()), "yyyy-MM-dd")
        self.fechaConsulta.setDisplayFormat("yyyy-MM-dd")
        self.fechaConsulta.setDate(qdate)
        self.fechaConsulta.setReadOnly(True)
        self.inputFrecRespiratoria.setText(str(ficha.getFrecRespiratoria()))
        self.inputFrecRespiratoria.setReadOnly(True)
        self.inputFrecCardiaca.setText(str(ficha.getFrecCardiaca()))
        self.inputFrecCardiaca.setReadOnly(True)
        self.inputPeso.setText(str(ficha.getPeso()))
        self.inputPeso.setReadOnly(True)
        self.inputEdad.setText(str(ficha.getEdad()))
        self.inputEdad.setReadOnly(True)
        self.inputTemp.setText(str(ficha.getTemp()))
        self.inputTemp.setReadOnly(True)
        
        tratamientosMostrar = ''
        for tratamiento in ficha.getTratamiento():
            item = str(tratamiento['nombreTratamiento'])
            self.inputCausaVisita.setText(str(tratamiento['causaVisita']))
            tratamientosMostrar = tratamientosMostrar + f' {item};'
        
        self.inputCausaVisita.setReadOnly(True)
        self.inputTratamientos.setText(tratamientosMostrar)
        self.inputTratamientos.setReadOnly(True)

        medicamentosMostrar = ''
        for medicamento in ficha.getMedicamentosConsulta():
            item = str(medicamento['nomMedicamento'])
            medicamentosMostrar = medicamentosMostrar + f' {item};'
            
        self.inputMedicamentos.setText(medicamentosMostrar)
        self.inputMedicamentos.setReadOnly(True)

        vacunasMostrar = ''
        for vacuna in ficha.getVacunasSuministradasConsulta():
            item = str(vacuna['nomVacuna'])
            vacunasMostrar = vacunasMostrar + f' {item};'

        self.inputVacunas.setText(vacunasMostrar)
        self.inputVacunas.setReadOnly(True)

        self.botonAgregarFichaOperacion.clicked.connect(lambda: self.crearFichaOperacion(mascota, ficha))
        self.botonAgregarFichaHosp.clicked.connect(lambda: self.crearFichaHospitalizacion(mascota, ficha))
        self.botonAgregarFichaSedacion.clicked.connect(lambda: self.crearFichaSedacion(mascota, ficha))
        

        self.botonVolver.clicked.connect(lambda : self.verScreenDatosTotal(mascota))
        self.botonAgregarFicha.setEnabled(False)

        if(ficha.getOperacion()):
            print(str(ficha.getOperacion()))
            self.botonAgregarFichaOperacion.setEnabled(False)

        if(ficha.getSedacion()):
            print(str(ficha.getSedacion()))
            self.botonAgregarFichaSedacion.setEnabled(False)

        if(ficha.getHospitalizacion()):
            print("hospitalizacion"+ str(ficha.getHospitalizacion()))
            self.botonAgregarFichaHosp.setEnabled(False)




    def crearFichaHospitalizacion(self, mascota : Mascota, ficha : FichaMedica):
        uic.loadUi("Complementos/formularioFichaHospitalizacion.ui", self)
        self.inputNombrePaciente.setText(mascota.getNombreMascota()) #se setean todos los valores ya obtenidos
        self.inputNombrePaciente.setReadOnly(True)
        self.inputPeso.setText(ficha.getPeso())
        self.inputPeso.setReadOnly(True)
        self.inputEspecie.setText(mascota.getEspecie())
        self.inputEspecie.setReadOnly(True)
        self.inputEdad.setText(ficha.getEdad())
        self.inputEdad.setReadOnly(True)
        self.inputRaza.setText(mascota.getRaza())
        self.inputRaza.setReadOnly(True)
        self.inputColor.setText(mascota.getColorMascota())
        self.inputColor.setReadOnly(True)


        self.botonAgregarFH.setEnabled(True)

        self.botonAgregarFH.clicked.connect(lambda : self.agregarFichaHospBd(mascota, ficha))

    def verFichaHosp(self, ficha: FichaMedica, mascota: Mascota):
        uic.loadUi("Complementos/formularioFichaHospitalizacion.ui", self)
        self.inputNombrePaciente.setText(mascota.getNombreMascota()) #se setean todos los valores ya obtenidos
        self.inputNombrePaciente.setReadOnly(True)
        self.inputPeso.setText(str(ficha.getPeso()))
        self.inputPeso.setReadOnly(True)
        self.inputEspecie.setText(mascota.getEspecie())
        self.inputEspecie.setReadOnly(True)
        self.inputEdad.setText(ficha.getEdad())
        self.inputEdad.setReadOnly(True)
        self.inputRaza.setText(mascota.getRaza())
        self.inputRaza.setReadOnly(True)
        self.inputColor.setText(mascota.getColorMascota())
        self.inputColor.setReadOnly(True)

        self.botonAgregarFH.setVisible(False)
        
        dicc = ficha.getHospitalizacionFicha()

        self.inputMotivoHospitalizacion.setPlainText(str(dicc["motivo"]))

        boton = QPushButton(self.contenedorBotonHosp)
        boton.setText('Volver')
        boton.setGeometry(0,0,131,51)
        boton.clicked.connect(lambda : self.verFichaMedica(ficha, mascota))

    def agregarFichaHospBd(self, mascota :Mascota, ficha : FichaMedica):
        
        hospitalizacion = True
        motivoHosp = self.inputMotivoHospitalizacion.toPlainText()
        idHosp = uuid.uuid4()
        
        sql = 'UPDATE fichamedica SET hospitalización=(%s) WHERE idFichaMedica = (%s)'
        mycursor.execute(sql, (hospitalizacion, str(ficha.getId())))
        db.commit()

        sql = 'INSERT INTO fichahospitalización VALUES (%s, %s, %s, %s)'
        mycursor.execute(sql, (str(idHosp), str(motivoHosp), str(ficha.getId()), str(ficha.getIdTabla())))
        db.commit()

        ficha.setHospitalizacion(hospitalizacion)
        hospDicc = {}
        for ficham in mascota.getTablaMedica().getFichas():
            if(ficham.getId() == ficha.getId()):
                ficham.setHospitalizacion(ficha.getOperacion)
                hospDicc = {
                    'id':idHosp,
                    'motivo':motivoHosp
                }
                ficham.setHospFichaLocal(hospDicc)

        self.volverACrearFicha(mascota, ficha)

    def crearFichaSedacion(self, mascota : Mascota, ficha : FichaMedica):
        
        uic.loadUi("Complementos/formularioFichaSedacion.ui", self)
        self.inputNombrePaciente.setText(mascota.getNombreMascota()) #se setean todos los valores ya obtenidos
        self.inputNombrePaciente.setReadOnly(True)
        self.inputEspecie.setText(mascota.getEspecie())
        self.inputEspecie.setReadOnly(True)
        self.inputRaza.setText(mascota.getRaza())
        self.inputRaza.setReadOnly(True)
        self.inputNomTutor.setText(mascota.getNombreTutor())
        self.inputNomTutor.setReadOnly(True)
        self.inputRut.setText(mascota.getRutTutor())
        self.inputRut.setReadOnly(True)
        self.inputNumTelefono.setText(mascota.getNumeroTelefono())
        self.inputNumTelefono.setReadOnly(True)
        self.inputDireccion.setText(mascota.getDireccion())
        self.inputDireccion.setReadOnly(True)


        self.botonAgregarFSedacion.setEnabled(True)

        self.botonAgregarFSedacion.clicked.connect(lambda : self.agregarFichaSedBd(mascota, ficha))

    def verFichaSedacion(self, ficha: FichaMedica, mascota:Mascota):
        uic.loadUi("Complementos/formularioFichaSedacion.ui", self)
        self.inputNombrePaciente.setText(mascota.getNombreMascota()) #se setean todos los valores ya obtenidos
        self.inputNombrePaciente.setReadOnly(True)
        self.inputEspecie.setText(mascota.getEspecie())
        self.inputEspecie.setReadOnly(True)
        self.inputRaza.setText(mascota.getRaza())
        self.inputRaza.setReadOnly(True)
        self.inputNomTutor.setText(mascota.getNombreTutor())
        self.inputNomTutor.setReadOnly(True)
        self.inputRut.setText(mascota.getRutTutor())
        self.inputRut.setReadOnly(True)
        self.inputNumTelefono.setText(mascota.getNumeroTelefono())
        self.inputNumTelefono.setReadOnly(True)
        self.inputDireccion.setText(mascota.getDireccion())
        self.inputDireccion.setReadOnly(True)

        self.checkAuth.setChecked(True)
        self.checkAuth.setEnabled(False)

        boton = QPushButton(self.contenedorBotonSedacion)
        boton.setText('Volver')
        boton.setGeometry(0,0,131,51)
        boton.clicked.connect(lambda : self.verFichaMedica(ficha, mascota))
    
    def agregarFichaSedBd(self, mascota :Mascota, ficha : FichaMedica):
        
        sedacion = True
        autorizacion = self.checkAuth.isChecked()
        idHosp = uuid.uuid4()
        
        sql = 'UPDATE fichamedica SET sedación=(%s) WHERE idFichaMedica = (%s)'
        mycursor.execute(sql, (sedacion, str(ficha.getId())))
        db.commit()

        sql = 'INSERT INTO fichasedación VALUES (%s, %s, %s, %s)'
        mycursor.execute(sql, (str(idHosp), autorizacion, str(ficha.getId()), str(ficha.getIdTabla())))
        db.commit()

        ficha.setSedacion(sedacion)

        sedDicc = {}
        for ficham in mascota.getTablaMedica().getFichas():
            if(ficham.getId() == ficha.getId()):
                ficham.setSedacion(ficha.getSedacion())
                sedDicc = {
                    'id':idHosp,
                    'autorizacion':autorizacion
                }
                ficham.setSedFichaLocal(sedDicc)

        self.volverACrearFicha(mascota, ficha)

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