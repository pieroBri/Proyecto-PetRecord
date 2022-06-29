import mysql.connector


db = mysql.connector.connect(
    user='piero',
    password='pieron123',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()

class FichaMedica:

    def __init__(self, id, sucursalVeterinaria, veterinarioACargo, fechaConsulta, operacion, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, sedacion, temp, idTabla):
        self.id = id
        self.idTabla = idTabla
        self.sucursalVeterinaria = sucursalVeterinaria
        self.veterinarioACargo = veterinarioACargo
        self.fechaConsulta = fechaConsulta
        self.medicamentosConsulta = []
        self.operacion = operacion
        self.operacionFicha = None
        self.vacunasSuministradasConsulta = []
        self.frecRespiratoria = frecRespiratoria
        self.frecCardiaca = frecCardiaca
        self.peso = peso
        self.edad = edad
        self.hospitalizacion = hospitalizacion
        self.hospitalizacionFicha = None
        self.sedacion = sedacion
        self.sedacionFicha = None
        self.tratamientoFicha = []
        self.temp = temp
        
    def editarFichaMedica(self):
        pass

    def crearFichaMedica(self):
        pass

    def editarFichaMedica(self):
        pass

    def crearFichaMedica(self):
        pass

#getters
    def getId(self):
        return self.id

    def getIdTabla(self):
        return self.idTabla
    
    def getSucursalVeterinaria(self):
        return self.sucursalVeterinaria

    def getTemp(self):
        return self.temp

    def getVeterinarioACargo(self):
        return self.veterinarioACargo

    def getFechaConsulta(self):
        return self.fechaConsulta

    def getMedicamentosConsulta(self):
        return self.medicamentosConsulta

    def getOperacion(self):
        return self.operacion

    def getOperacionFicha(self):
        return self.operacionFicha
    
    def getVacunasSuministradasConsulta(self):
        return self.vacunasSuministradasConsulta

    def getFrecRespiratoria(self):
        return self.frecRespiratoria
    
    def getFrecCardiaca(self):
        return self.frecCardiaca
    
    def getPeso(self):
        return self.peso
    
    def getEdad(self):
        return self.edad
    
    def getHospitalizacion(self):
        return self.hospitalizacion
    
    def getHospitalizacionFciha(self):
        return self.hospitalizacionFicha
    
    def getSedacion(self):
        return self.sedacion
    
    def getSedacioFicha(self):
        return self.sedacionFicha
    
    def getTratamiento(self):
        return self.tratamientoFicha

#setters 

    def setId(self, id):
        self.id = id

    def setIdTabla(self, idTabla):
        self.idTabla = idTabla
    
    def setSucursalVeterinaria(self, sucursalVeterinaria):
        self.sucursalVeterinaria = sucursalVeterinaria
    
    def setVeterinarioACargo(self, veterinarioACargo):
        self.veterinarioACargo = veterinarioACargo
    
    def setFechaConsulta(self, fechaConsulta):
        self.fechaConsulta = fechaConsulta

    def setOperacion(self, operacion):
        self.operacion = operacion

    def setFrecRespiratoria(self, frecRespiratoria):
        self.frecRespiratoria = frecRespiratoria

    def setFrecCardiaca(self, frecCardiaca):
        self.frecCardiaca = frecCardiaca

    def setPeso(self, peso):
        self.peso = peso

    def setEdad(self, edad):
        self.edad = edad

    def setHospitalizacion(self, hospitalizacion):
        self.hospitalizacion = hospitalizacion

    def setSedacion(self, sedacion):
        self.sedacion = sedacion

    def setTemp(self, temp):
        self.temp = temp

    def setOpFicha(self):
        if(self.operacion == 1):
            sql = 'SELECT * FROM fichaOperación WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.id),))
            opFicha = mycursor.fetchone()
            if(opFicha[3] == 1):
                aut = True
            else:
                aut = False
            self.operacionFicha = {
                'id':opFicha[0],
                'diagnostico':opFicha[1],
                'cirugiaARealizar':opFicha[2],
                'autTutor': aut
            }
    
    def setMedicamentosConsulta(self):
        sql = 'SELECT * FROM medicamentosconsulta WHERE FichaMedica_idFichaMedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        medicamentos = mycursor.fetchall()
        for medicamento in medicamentos:
            med = {
            'id' : medicamento[0],
            'nomMedicamento' : medicamento[1],
            }
            self.medicamentosConsulta.append(med)
        
    def setVacFicha(self):
        sql = 'SELECT * FROM VacunasSuministradasConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        vacunas = mycursor.fetchall()
        for vacuna in vacunas:
            vac = {
            'id' : vacuna[0],
            'nomVacuna' : vacuna[1],
            }
            self.vacunasSuministradasConsulta.append(vac)

    def setHospFicha(self):
        if(self.hospitalizacion == 1):
            sql = 'SELECT * FROM FichaHospitalización WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.id),))
            hospiFicha = mycursor.fetchone()
            self.hospitalizacionFicha = {
                'id':hospiFicha[0],
                'motivo':hospiFicha[1],
            }

    def setSedFicha(self):
        if (self.sedacion == 1):
            sql = 'SELECT * FROM FichaSedación WHERE FichaMedica_idFichaMedica = (%s)'
            mycursor.execute(sql, (str(self.id),))
            sedacion = mycursor.fetchone()
            if(sedacion[1] == 1):
                aut = True
            else:
                aut = False
            self.sedacionFicha =  {
                'id':sedacion[0],
                'autorizacion':aut,
            }

    def setTratamiento(self):
        sql = 'SELECT * FROM TratamientosConsulta WHERE FichaMedica_idFichaMedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        tratamientos = mycursor.fetchall()
        for tratamiento in tratamientos:
            trat = {
            'id' : tratamiento[0],
            'nombreTratamiento': tratamiento[1],
            'causaVisita' : tratamiento[2],
            }
            self.tratamientoFicha.append(trat)