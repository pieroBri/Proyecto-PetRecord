#ESTA ES LA CLASE MAIN, IMPORTAR LAS DEMAS CLASES ACA
from tkinter import *

class TerminalVeterinario:

    def __init__(self, id, tokenActivacion, mascotas):
        self.id = id
        self.tokenActivacion = tokenActivacion
        self.mascotas = mascotas

    def ingresarMascota(self, mascotaNueva):
        self.mascotas.append(mascotaNueva)

    def verificarLlaveConServidor(self):
        pass

    def verificarMascota(self):
        pass

    def validarConexionInternet(self):
        pass

    def activarToken(self):
        pass

    def consultaBDToken(self):
        pass

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