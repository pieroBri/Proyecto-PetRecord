#ESTA ES LA CLASE MAIN, IMPORTAR LAS DEMAS CLASES ACA
from tkinter import *
import os
import os.path
import uuid

class TerminalVeterinario:

    def __init__(self, id, tokenActivacion, idVeterinaria, nombreVeterinaria):
        self.id = id
        self.tokenActivacion = tokenActivacion
        self.idVeterinaria = idVeterinaria
        self.nombreVeterinaria = nombreVeterinaria
        self.mascotas = None

    def validarConexionInternet(self):
        pass

    def validarLlaveConServidor(self):
        pass

    def activarTokenDeActivacion(self):
        pass

    def consultaBDTokenDeActivacion(self):
        pass

    def validarTokenDeActivacion(self):
        pass

    def ingresarMascotaAlSistema(self, mascotaNueva):
        self.mascotas.append(mascotaNueva)

    def verificarMascotaEnSistema(self):
        pass

    def agregarFichaMedicaGeneral():
        pass
    
    def editarFichaMedicaGeneral():
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
                lineasTexto = f.readlines()
                for i in lineasTexto:
                    print(i)
        else:
            with open("infoTerminal.txt", "w") as f: #si no existe el archivo lo creamos y le damos el formato default
                idRand = uuid.uuid4()
                print(idRand)
                f.write(f"id = {idRand}")
                
root = Tk()
root.title('My Pet Record :)')
root.geometry("1280x720")
root.configure(background="#2C794B")

#Crear campos de entrada
alergias = Entry(root, width=30)
alergias.grid(row=0, column=1)
registro_Operaciones = Entry(root, width=30)
registro_Operaciones.grid(row=1, column=1)
vacunas_Suministradas = Entry(root, width=30)
vacunas_Suministradas.grid(row=2, column=1)

#Crear frame para fichas
fichas_Frame = LabelFrame(root, text="Fichas médicas mascota",  padx=25, pady=25)
fichas_Frame.grid(row=3, column=0, padx=10, pady=10)

#Crear boton de agrear ficha
btt_Agregar_Ficha = Button(fichas_Frame, text="Agregar Ficha")
btt_Agregar_Ficha.pack()

#Crear labels de los campos de entrada
alergias_Label = Label(root, text="Alergias :")
alergias_Label.grid(row=0, column=0)
registro_Operaciones_Label = Label(root, text="Registro Operaciones")
registro_Operaciones_Label.grid(row=1, column=0)
vacunas_Suministradas_Label = Label(root, text="Vacunas Suministradas")
vacunas_Suministradas_Label.grid(row=2, column=0, padx=50)

root.mainloop()

