# -*- coding: utf-8 -*-
"""
TaskDesk - Gestor de Tareas Personales
---------------------------------------
Aplicacion de escritorio (Python + Tkinter), independiente y autocontenida:
no depende de ningun otro sistema, base de datos externa ni conexion a
internet. Permite agregar tareas con prioridad, marcarlas como completadas,
eliminarlas y guarda todo automaticamente en un archivo local (tareas.json)
en la misma carpeta del programa.

Autor: Alejandro Perez Alcantara
Materia: Aplicaciones Web Progresivas - 10 D
Subproducto No. 3 - Aplicacion de Escritorio
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import datetime

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas.json")

VERDE = "#1f7a3d"
VERDE_OSCURO = "#155a2c"
AZUL = "#1c3f66"
FONDO = "#f4f8f5"
TEXTO = "#22252a"
GRIS = "#6b7280"

PRIORIDADES = ["Alta", "Media", "Baja"]


def cargar_tareas():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def guardar_tareas(tareas):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)


class TaskDeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskDesk - Gestor de Tareas Personales")
        self.root.geometry("480x600")
        self.root.configure(bg=FONDO)
        self.root.resizable(False, False)

        self.tareas = cargar_tareas()

        self._build_header()
        self._build_form()
        self._build_lista()
        self._build_resumen()
        self._refrescar_lista()

    # ---------- UI ----------
    def _build_header(self):
        header = tk.Frame(self.root, bg=VERDE, height=90)
        header.pack(fill="x")
        tk.Label(header, text="TaskDesk", bg=VERDE, fg="white",
                  font=("Segoe UI", 18, "bold")).pack(pady=(16, 0))
        tk.Label(header, text="Gestor de tareas personales (100% local, sin internet)",
                  bg=VERDE, fg="#e3f2e8", font=("Segoe UI", 10)).pack(pady=(0, 14))

    def _build_form(self):
        form = tk.Frame(self.root, bg=FONDO, padx=24, pady=16)
        form.pack(fill="x")

        tk.Label(form, text="Nueva tarea", bg=FONDO, fg=TEXTO,
                  font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        self.entry_tarea = ttk.Entry(form, width=34)
        self.entry_tarea.grid(row=1, column=0, columnspan=2, sticky="we", pady=(2, 10))

        tk.Label(form, text="Prioridad", bg=FONDO, fg=TEXTO,
                  font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
        self.combo_prioridad = ttk.Combobox(form, values=PRIORIDADES, state="readonly", width=12)
        self.combo_prioridad.set("Media")
        self.combo_prioridad.grid(row=3, column=0, sticky="w", pady=(2, 10))

        btn = tk.Button(form, text="Agregar tarea", bg=VERDE, fg="white",
                          font=("Segoe UI", 10, "bold"), relief="flat", padx=10, pady=6,
                          activebackground=VERDE_OSCURO, activeforeground="white",
                          command=self.agregar_tarea)
        btn.grid(row=3, column=1, sticky="we", pady=(2, 10), padx=(10, 0))
        form.grid_columnconfigure(1, weight=1)

    def _build_lista(self):
        frame = tk.Frame(self.root, bg="white", padx=12, pady=12,
                           highlightbackground="#d7e4da", highlightthickness=1)
        frame.pack(fill="both", expand=True, padx=24, pady=(4, 10))

        tk.Label(frame, text="Mis tareas (doble clic para completar)", bg="white",
                  fg=TEXTO, font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.listbox = tk.Listbox(frame, height=12, font=("Segoe UI", 10),
                                    selectbackground=VERDE, activestyle="none")
        self.listbox.pack(fill="both", expand=True, pady=(6, 6))
        self.listbox.bind("<Double-Button-1>", self.completar_tarea)

        btn_eliminar = tk.Button(frame, text="Eliminar tarea seleccionada", bg=AZUL, fg="white",
                                   font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=5,
                                   activebackground="#12283f", activeforeground="white",
                                   command=self.eliminar_tarea)
        btn_eliminar.pack(fill="x")

    def _build_resumen(self):
        self.lbl_resumen = tk.Label(self.root, text="", bg=FONDO, fg=GRIS,
                                      font=("Segoe UI", 9, "italic"))
        self.lbl_resumen.pack(anchor="w", padx=24, pady=(0, 12))

    # ---------- Logica ----------
    def agregar_tarea(self):
        texto = self.entry_tarea.get().strip()
        if not texto:
            messagebox.showwarning("Tarea vacia", "Escribe una descripcion antes de agregar la tarea.")
            return
        tarea = {
            "texto": texto,
            "prioridad": self.combo_prioridad.get(),
            "completada": False,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.tareas.append(tarea)
        guardar_tareas(self.tareas)
        self.entry_tarea.delete(0, "end")
        self._refrescar_lista()

    def completar_tarea(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.tareas[idx]["completada"] = not self.tareas[idx]["completada"]
        guardar_tareas(self.tareas)
        self._refrescar_lista()

    def eliminar_tarea(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Selecciona una tarea", "Elige una tarea de la lista para eliminarla.")
            return
        idx = sel[0]
        del self.tareas[idx]
        guardar_tareas(self.tareas)
        self._refrescar_lista()

    def _refrescar_lista(self):
        self.listbox.delete(0, "end")
        for t in self.tareas:
            marca = "[X]" if t["completada"] else "[ ]"
            self.listbox.insert("end", f"{marca} ({t['prioridad']}) {t['texto']}")
        pendientes = sum(1 for t in self.tareas if not t["completada"])
        completadas = sum(1 for t in self.tareas if t["completada"])
        self.lbl_resumen.config(
            text=f"Pendientes: {pendientes}   |   Completadas: {completadas}   |   Archivo: {os.path.basename(DATA_PATH)}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskDeskApp(root)
    root.mainloop()
