import tkinter as tk
from tkinter import messagebox
import sqlite3



#crea la base de datos a un lado del script
conn = sqlite3.connect("contactos.db")
cursor = conn.cursor()
cursor.execute(""" 

CREATE TABLE IF NOT EXISTS contactos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               telefono TEXT,
               correo TEXT    
)

 """)

conn.commit()


#funciones 
def agregar_contacto():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    correo = entry_correo.get()

    if nombre:
        cursor.execute("INSERT INTO contactos (nombre, telefono, correo) values (?,?,?)", (nombre, telefono, correo))

        conn.commit()
        mostrar_contactos()
        limpiar_campos()

    else:
        messagebox.showwarning("Campo Obligatorio", "El nombre es obligatorio")



def monstrar_contactos():
    lista.delete(0, tk.END)
    cursor.execute("SELECT * FROM contactos")
    for conatcto in cursor.fetchall():
        lista.insert(tk.END, conatcto)


def seleccionar_contacto():
    global id_contacto
    if lista.curselection():
        index = lista.curselection()[0]
        contacto = lista.get(index)
        id_contacto = contacto[0]
        entry_nombre.delete(0, tk.END)
        entry_nombre



























#interfaz 
app = tk.Tk()
app.title("Agenda de Contactos")
app.geometry("500x400")

#variables 
id_contacto = None

#Entradas
tk.Label(app, text="Nombre: ").pack()
entry_nombre = tk.Entry(app)
entry_nombre.pack()



tk.Label(app, text="Telefono: ").pack()
entry_telefono = tk.Entry(app)
entry_telefono.pack();


tk.Label(app, text="Correo: ").pack()
entry_correo = tk.Entry(app)
entry_correo.pack()

#Botones
tk.Button(app, text="Agregar", command=agregar_contacto).pack(pady=5)
tk.Button(app, text="Actualizar", command=actualizar_contacto).pack(pady=5)
tk.Button(app, text="Eliminar", command=eliminar_contacto).pack(pady=5)
tk.Button(app, text="LImpiar", command=limpiar_campos).pack(pady=5)



#Lisdta de los contactos
lista = tk.LIstbox(app)
lista.pack(fill=tk.BOTH, expand=True)
lista.bind("<<ListboxSelect>>", seleccionar_contacto)

#Mostrar contactos al inicio
mostrar_contactos()



#ejecuta las ventasnitas
app.mainloop()