from key_generator.key_generator import generate
import uuid
import mysql.connector

flag=True


idBD = uuid.uuid4()

nombreVet = input('Ingresar nombre veterinaria : ')

while flag:
    num = input("Ingrese cantidad de llaves : ")
    try:
        val = int(num)
        if(int(num)<10 and int(num)>0) :
            key = [None]*int(num)
            for i in range(int(num)) :
                key[i] = generate(4, '-', 5, 5, 'hex', 'none', [], None).get_key()
                print(key[i])
            flag=False
        else :
            print('Ingrese numero valido')
    except ValueError:
        print("Ingrese numero valido")


db = mysql.connector.connect(user='root', password='root', host='186.79.170.186', port='3306', database='mydb')

mycursor = db.cursor()
sql = f'INSERT INTO veterinaria VALUES ("{idBD}", "{nombreVet}")'
mycursor.execute(sql)
db.commit()

for i in range(len(key)):
    sql = f'INSERT INTO keysactivación VALUES ("{key[i]}","{idBD}", "{nombreVet}")'
    mycursor.execute(sql)
    db.commit()

mycursor.execute('select * from keysactivación')
resultado = mycursor.fetchall()
print(resultado)


