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



def mostrar_contactos():
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
        entry_nombre.insert(tk.END, contacto[1])
        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(tk.END, contacto[2])
        entry_correo.delete(0, tk.END)
        entry_correo.insert(tk.END, contacto[3])



def actualizar_contacto():


    if id_contacto is not None:

        cursor.execute("""UPDATE contactos SET nombre=?, telefono=?, correo=? WHERE id=?""", (entry_nombre.get(), entry_correo.get(), entry_telefono.get(), id_contacto))
    
        conn.commit()
        mostrar_contactos()
        limpiar_campos()

    else:
        messagebox.showinfo("Selecciona", "Primero selecciona un contacto para actualizar")


def eliminar_contacto():
    if id_contacto is not None:
        cursor.execute("DELETE FROM contactos WHERE id=?", (id_contacto,))
        conn.commit()
        mostrar_contactos()
        limpiar_campos()

    else:
        messagebox.showinfo("Selecciona", "Selecciona un contacto a eliminar.")

def limpiar_campos():
    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    global id_contacto
    id_contacto = None
    

























#interfaz 
app = tk.Tk()
app.title("Agenda de Contactos")
app.geometry("500x400")


#declarando los frames
form = tk.Frame(app)
form.pack(pady=20)

#variables 
id_contacto = None

#Entradas
tk.Label(form, text="Nombre: ").grid(row=0, column=0, sticky="e")
entry_nombre = tk.Entry(form)
entry_nombre.grid(row=0, column=1)



tk.Label(form, text="Telefono: ").grid(row=1, column=0, sticky="e")
entry_telefono = tk.Entry(form)
entry_telefono.grid(row=1, column=1, pady=10);


tk.Label(form, text="Correo: ").grid(row=2, column=0, sticky="e")
entry_correo = tk.Entry(form)
entry_correo.grid(row=2, column=1, pady=5)



buttons= tk.Frame(app)
buttons.pack(pady=20)
#Botones
tk.Button(buttons, text="Agregar", command=agregar_contacto).grid(row=0, column=0, padx=5)
tk.Button(buttons, text="Actualizar", command=actualizar_contacto).grid(row=0, column=1, padx=5)
tk.Button(buttons, text="Eliminar", command=eliminar_contacto).grid(row=0, column=2, padx=5)
tk.Button(buttons, text="LImpiar", command=limpiar_campos).grid(row=0, column=3, padx=5)



#Lisdta de los contactos
lista = tk.Listbox(app)
lista.pack(fill=tk.BOTH, expand=True)
lista.bind("<<ListboxSelect>>", seleccionar_contacto)

#Mostrar contactos al inicio
mostrar_contactos()



#ejecuta las ventasnitas
app.mainloop()