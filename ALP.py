import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

class AppOrganizer:
    def __init__(self, filename='apps.json'):
        self.filename = filename
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
                for category, apps in self.data.items():
                    if isinstance(apps, list):
                        self.data[category] = {app: app for app in apps}
        else:
            self.data = {}

    def save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_category(self, category):
        if category not in self.data:
            self.data[category] = {}
            self.save_data()

    def remove_category(self, category):
        if category in self.data:
            del self.data[category]
            self.save_data()

    def rename_category(self, old_name, new_name):
        if old_name in self.data and new_name not in self.data:
            self.data[new_name] = self.data.pop(old_name)
            self.save_data()

    def add_program(self, category):
        if category in self.data:
            filepath = filedialog.askopenfilename(title='Selecciona un programa')
            if filepath:
                program_name = os.path.basename(filepath)
                self.data[category][program_name] = filepath
                self.save_data()

    def remove_program(self, category, program):
        if category in self.data and program in self.data[category]:
            del self.data[category][program]
            self.save_data()

    def rename_program(self, category, old_name, new_name):
        if category in self.data and old_name in self.data[category]:
            self.data[category][new_name] = self.data[category].pop(old_name)
            self.save_data()

    def open_program(self, category, program):
        try:
            path = self.data[category][program]
            subprocess.Popen(path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el programa: {e}")

organizer = AppOrganizer()

# Interfaz gráfica
root = tk.Tk()
root.title("Organizador de Aplicaciones")
root.geometry("700x600")

# Actualización de listas
def update_category_list():
    category_list.delete(0, tk.END)
    for category in organizer.data.keys():
        category_list.insert(tk.END, category)

def update_program_list(category):
    program_list.delete(0, tk.END)
    if category in organizer.data:
        for program in organizer.data[category].keys():
            program_list.insert(tk.END, program)

# Selección de categoría
def on_category_select(event):
    selection = category_list.curselection()
    if selection:
        category = category_list.get(selection[0])
        update_program_list(category)

# Botones de categorías
def add_category():
    category = category_entry.get()
    if category:
        organizer.add_category(category)
        update_category_list()

def remove_category():
    category = category_list.get(tk.ACTIVE)
    organizer.remove_category(category)
    update_category_list()
    program_list.delete(0, tk.END)

def rename_category():
    category = category_list.get(tk.ACTIVE)
    new_name = category_entry.get()
    if category and new_name:
        organizer.rename_category(category, new_name)
        update_category_list()

# Botones de programas
def add_program():
    category = category_list.get(tk.ACTIVE)
    if category:
        organizer.add_program(category)
        update_program_list(category)

def remove_program():
    category = category_list.get(tk.ACTIVE)
    program = program_list.get(tk.ACTIVE)
    organizer.remove_program(category, program)
    update_program_list(category)

def rename_program():
    category = category_list.get(tk.ACTIVE)
    program = program_list.get(tk.ACTIVE)
    new_name = program_entry.get()
    if category and program and new_name:
        organizer.rename_program(category, program, new_name)
        update_program_list(category)

def open_program():
    category = category_list.get(tk.ACTIVE)
    program = program_list.get(tk.ACTIVE)
    if category and program:
        organizer.open_program(category, program)

# Elementos gráficos
category_list = tk.Listbox(root, width=30, height=15)
category_list.grid(row=0, column=0, padx=10, pady=10)
category_list.bind('<<ListboxSelect>>', on_category_select)

program_list = tk.Listbox(root, width=50, height=15)
program_list.grid(row=0, column=1, padx=10, pady=10)

category_entry = tk.Entry(root)
category_entry.grid(row=1, column=0, padx=5, pady=5)
program_entry = tk.Entry(root)
program_entry.grid(row=1, column=1, padx=5, pady=5)

add_cat_btn = tk.Button(root, text="Agregar Categoría", command=add_category)
add_cat_btn.grid(row=2, column=0, padx=5, pady=5)

remove_cat_btn = tk.Button(root, text="Eliminar Categoría", command=remove_category)
remove_cat_btn.grid(row=3, column=0, padx=5, pady=5)

rename_cat_btn = tk.Button(root, text="Modificar Categoría", command=rename_category)
rename_cat_btn.grid(row=4, column=0, padx=5, pady=5)

add_prog_btn = tk.Button(root, text="Agregar Programa", command=add_program)
add_prog_btn.grid(row=2, column=1, padx=5, pady=5)

remove_prog_btn = tk.Button(root, text="Eliminar Programa", command=remove_program)
remove_prog_btn.grid(row=3, column=1, padx=5, pady=5)

rename_prog_btn = tk.Button(root, text="Modificar Programa", command=rename_program)
rename_prog_btn.grid(row=4, column=1, padx=5, pady=5)

open_prog_btn = tk.Button(root, text="Abrir Programa", command=open_program)
open_prog_btn.grid(row=5, column=1, padx=5, pady=5)

update_category_list()
root.mainloop()

