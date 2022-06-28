from fichaMedica import FichaMedica

import mysql.connector


db = mysql.connector.connect(
    user='piero',
    password='pieron123',
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
            ficham = FichaMedica(ficha[0],ficha[1],ficha[2],ficha[3],ficha[4],ficha[5],ficha[6],ficha[7],ficha[8],ficha[9],ficha[10],ficha[11])
            ficham.setOpFicha()
            ficham.setmedicamentosConsulta()
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

    def setFcihas(self, fichas):
        self.fichas.append(fichas)
    
    def setAlergias(self, alergias):
        self.alergias = alergias
    
    def setRegistroDeOperaciones(self, registroDeOperaciones):
        self.registroDeOperaciones = registroDeOperaciones