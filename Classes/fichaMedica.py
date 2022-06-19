class FichaMedica:

    def __init__(self, id, idTabla, sucursalVeterinaria, veterinarioACargo, fechaConsulta, medicamentosConsulta, causaDeLaVisita, operacion, operacionFicha, vacunasSuministradasConsulta, frecRespiratoria, frecCardiaca, peso, edad, hospitalizacion, hospitalizacionFicha, sedacion, sedacionFicha):
        self.id = id
        self.idTabla = idTabla
        self.sucursalVeterinaria = sucursalVeterinaria
        self.veterinarioACargo = veterinarioACargo
        self.fechaConsulta = fechaConsulta
        self.medicamentosConsulta = medicamentosConsulta
        self.causaDeLaVisita = causaDeLaVisita
        self.operacion = operacion
        self.operacionFicha = operacionFicha
        self.vacunasSuministradasConsulta = vacunasSuministradasConsulta
        self.frecRespiratoria = frecRespiratoria
        self.frecCardiaca = frecCardiaca
        self.peso = peso
        self.edad = edad
        self.hospitalizacion = hospitalizacion
        self.hospitalizacionFicha = hospitalizacionFicha
        self.sedacion = sedacion
        self.sedacionFicha = sedacionFicha

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

    def getVeterinarioACargo(self):
        return self.veterinarioACargo

    def getFechaConsulta(self):
        return self.fechaConsulta

    def getMedicamentosConsulta(self):
        return self.medicamentosConsulta

    def getCausaDeLaVisita(self):
        return self.causaDeLaVisita

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
    
    def setMedicamentoConsulta(self, medicamentosConsulta):
        self.medicamentosConsulta = medicamentosConsulta

    def setCausaDeLaVisita(self, causaDeLaVisita):
        self.causaDeLaVisita = causaDeLaVisita

    def setOperacion(self, operacion):
        self.operacion = operacion

    def setOperacionFicha(self, operacionFicha):
        self.operacionFicha = operacionFicha

    def setVacunasSuministradasConsulta(self, vacunasSuministradasConsulta):
        self.vacunasSuministradasConsulta = vacunasSuministradasConsulta

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

    def setHospitalizacionFicha(self, hospitalizacionFicha):
        self.hospitalizacionFicha = hospitalizacionFicha

    def setSedacion(self, sedacion):
        self.sedacion = sedacion

    def setSedacionFicha(self, sedacionFicha):
        self.sedacionFicha = sedacionFicha
    