import fichaMedica

class TablaMedica:

    def __init__(self, id, alergias, registroDeOperaciones, vacunasSuministradas):
        self.id = id
        self.fichas = None
        self.alergias = alergias
        self.registroDeOperaciones = registroDeOperaciones #string
        self.vacunasSuministradas = vacunasSuministradas #string

    def crearFichaMedicaConsulta(self):
        pass

    def editarFichaMedicaConsulta(self):
        pass

    def mostrarFichasMedicas(self):
        pass

    def validarFormatoDatos(self):
        pass

    def solicitudConexionServCrear(self):
        pass

    def solicitudConexionServEditar(self):
        pass

    def solicitudConexionServMostrar(self):
        pass

    def getFichas(self):
        return self.fichas

    def getId(self):
        return self.id

    def getAlergias(self):
        return self.alergias
    
    def getRegistroDeOperaciones(self):
        return self.registroDeOperaciones
    
    def getVacunasSuministradas(self):
        return self.vacunasSuministradas
    
    def getId(self):
        return self.id
#setter
    def setId(self, id):
        self.id = id

    def setFcihas(self, fichas):
        self.fichas.append(fichas)
    
    def setAlergias(self, alergias):
        self.alergias = alergias
    
    def setRegistroDeOperaciones(self, registroDeOperaciones):
        self.registroDeOperaciones = registroDeOperaciones