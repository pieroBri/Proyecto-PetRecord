from tablaMedica import TablaMedica


class Mascota:

    def __init__(self, id, nombre, especie, color, raza, nombreTutor, rutTutor, numeroTelefono, direccion, tablaMedica):
        self.nombre = nombre
        self.id = id
        self.especie = especie
        self.tablaMedica = tablaMedica
        self.color = color
        self.raza = raza
        self.nombreTutor = nombreTutor
        self.rutTutor = rutTutor
        self.numeroTelefono = numeroTelefono
        self.direccion = direccion

    def editarInfoBasicaMascota(self):
        pass

    def crearFichaMedicaConsulta(self,fichaMedica):
        pass

    def editarFichaMedicaConsulta(self,fichaMedica):
        pass

    def buscarFichaMedicaConsulta(self):
        pass

    def validarFormatoDatosFichaMedicaGeneral():
        pass

    def validarFormatoDatosFichaMedica():
        pass

    def solicitudServCrear():
        pass

    def solicitudServEditar():
        pass

    def getId(self):
        return self.id

    def getTablaMedica(self) -> TablaMedica:
        return self.tablaMedica
    
    def getNombreMascota(self):
        return self.nombre

    def getColorMascota(self):
        return self.color

    def getEspecie(self):
        return self.especie

    def getRaza(self):
        return self.raza

    def getNombreTutor(self):
        return self.nombreTutor

    def getRutTutor(self):
        return self.rutTutor

    def getNumeroTelefono(self):
        return self.numeroTelefono

    def getDireccion(self):
        return self.direccion
    #faltan Getter y Setters