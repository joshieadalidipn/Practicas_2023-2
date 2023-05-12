import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
from pyswip import Prolog

# Prolog setup
prolog = Prolog()
prolog.consult('taxonomy.pl')


# Definición de funciones
def set_image(path):
    """Configura la imagen a mostrar en el panel."""
    img = Image.open(path)
    img = img.resize((250, 250), resample=Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img


def show_image(event):
    """Muestra la imagen del animal seleccionado."""
    selection = listbox.curselection()
    if selection:
        selected_animal = listbox.get(selection[0])
        img_path = next(prolog.query(f"frame({selected_animal}, _, Path)"))['Path']
        img_path = img_path[img_path.find('(') + 1:img_path.find(')')]
        set_image('img/' + img_path)


def query_prolog():
    # Obtener el término de búsqueda ingresado por el usuario
    input_str = entry.get()

    try:
        # Extraer la propiedad de búsqueda del término de búsqueda
        colon_idx = input_str.find(':')
        if colon_idx == -1:
            raise ValueError(f"No se especificó la propiedad de búsqueda en '{input_str}'")
        search_prop = input_str[:colon_idx]
        search_term = input_str[colon_idx+1:].strip()

        # Construir la consulta de Prolog
        query_str = f"frame(Animal, _, properties(ListaPropiedades), imagen(Path)), member({search_prop}('{search_term}'), ListaPropiedades)"
        query = prolog.query(query_str)
        results = list(query)

        # Actualizar la lista de animales
        listbox.delete(0, tk.END)
        for result in results:
            result_animal = result['Animal']
            listbox.insert(tk.END, result_animal)

            # Si la consulta incluye la propiedad 'imagen', mostramos la imagen correspondiente
            img_path = result['Path']
            img_path = img_path[img_path.find('(') + 1:img_path.find(')')]
            set_image('img/' + img_path)

        # Mostrar un mensaje de error si no se encontraron resultados
        if len(results) == 0:
            messagebox.showerror("Error", f"No se encontraron resultados para '{input_str}'")

    except Exception as ex:
        error = f"Consulta inválida ({ex})"
        print(error)
        messagebox.showerror("Error", error)



def list_all():
    """Lista todos los animales en la base de datos Prolog."""
    listbox.delete(0, tk.END)
    animals = list(prolog.query("frame(Animal, _, Image)"))
    for animal in animals:
        listbox.insert(tk.END, animal['Animal'])
    listbox.bind('<<ListboxSelect>>', show_image)


# Configuración de la interfaz gráfica
root = tk.Tk()
entry = tk.Entry(root)
button = tk.Button(root, text="Consultar", command=query_prolog)
list_button = tk.Button(root, text="Listar todos", command=list_all)
listbox = tk.Listbox(root)
panel = tk.Label(root)

# Llamar a la función list_all al iniciar
list_all()

# Ajustamos la geometría de los widgets con grid
entry.grid(row=0, column=0, sticky="W")
button.grid(row=0, column=1, sticky="W")
list_button.grid(row=0, column=2, sticky="W")
listbox.grid(row=1, column=0, rowspan=2, sticky="NS")
panel.grid(row=1, column=1, rowspan=2, padx=10, pady=10)

# Ajustamos el tamaño de las columnas y filas
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
