from fichaMedica import FichaMedica

import mysql.connector


db = mysql.connector.connect(
    user='root',
    password='root',
    host='localhost',
    database='mydb',
    port='3306'
)

mycursor = db.cursor()


class TablaMedica:

    def __init__(self, id, alergias, registroDeOperaciones, vacunasSuministradas):
        self.id = id
        self.fichas = []
        self.alergias = alergias
        self.registroDeOperaciones = registroDeOperaciones #string
        self.vacunasSuministradas = vacunasSuministradas #string
    

    def cargarFichas(self):
        sql = 'SELECT * FROM fichaMedica WHERE Tablamedica_idTablamedica = (%s)'
        mycursor.execute(sql, (str(self.id),))
        fichas = mycursor.fetchall()
        for ficha in fichas:
            ficham = FichaMedica(ficha[0],ficha[1],ficha[2],ficha[3],ficha[4],ficha[5],ficha[6],ficha[7],ficha[8],ficha[9],ficha[10],ficha[11], ficha[12])
            ficham.setOpFicha()
            ficham.setMedicamentosConsulta()
            ficham.setVacFicha()
            ficham.setHospFicha()
            ficham.setSedFicha()
            ficham.setTratamiento()
            self.fichas.append(ficham)


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

    def setOpFichaLocal(self, idFicha, opDicc, operacion):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setOperacion(operacion)
                ficha.setOpFichaLocal(opDicc)

    def setVacFichaLocal(self, idFicha, vacDicc):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setVacFichaLocal(vacDicc)
    
    def setHospFichaLocal(self, idFicha, hospFicha, hosp):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setHospitalizacion(hosp)
                ficha.setHospFichaLocal(hospFicha)
    
    def setSedFichaLocal(self, idFicha, sedDicc, sedacion):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setSedacion(sedacion)
                ficha.setSedFichaLocal(sedDicc)
    
    def setTratamientoLocal(self, idFicha, tratamiento):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setTratamientoLocal(tratamiento)

    def setMedicamentosConsultaLocal(self, idFicha, medicamentos):
        for ficha in self.fichas:
            if ficha.getId() == idFicha:
                ficha.setMedicamentosConsultaLocal(medicamentos)


    def getFichas(self) -> list:
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

    def setFichas(self, fichas):
        self.fichas.append(fichas)
    
    def setAlergias(self, alergias):
        self.alergias = alergias
    
    def setRegistroDeOperaciones(self, registroDeOperaciones):
        self.registroDeOperaciones = registroDeOperaciones