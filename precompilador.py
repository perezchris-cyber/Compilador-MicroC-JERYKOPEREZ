import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

class Pre_compilador:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.config(bg="green")
        self.current_file = None
        self.modified = False
        self.create_widgets()
        self.update_title()

    def create_widgets(self):
        # Frame de botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        buttons = [
            ("Nuevo", self.nuevo_archivo),
            ("Abrir", self.abrir_archivo),
            ("Guardar", self.guardar_archivo),
            ("Salir", self.salir),
            ("Editar", self.editar),
            ("Compilar", self.compilar),
            ("Ayuda", self.ayuda)
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, width=10, command=command)
            btn.pack(side=tk.LEFT)

        # código
        code_frame = tk.Frame(self.root)
        code_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(code_frame, text="Código:", anchor="w").pack(fill=tk.X)

        self.code_text = scrolledtext.ScrolledText(code_frame, wrap=tk.NONE, height=1, bg="skyblue")
        self.code_text.pack(fill=tk.BOTH, expand=True)

        # resultados
        result_frame = tk.Frame(self.root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(result_frame, text="Resultados de compilación:", anchor="w").pack(fill=tk.X)

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=1, bg="skyblue")
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Barra de estado
        self.status_bar = tk.Label(self.root, text="Archivo: Ninguno", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="skyblue")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.code_text.bind("<<Modified>>", self.on_text_modified)

    # NOMBRE DE LA VENTANA CON LA RUTA QUE SE ESTA TRABAJANDO
    def update_title(self):
        if self.current_file:
            nombre_mostrar = self.current_file
        else:
            nombre_mostrar = "Sin título"
        titulo = f"PRE COMPILADOR - {nombre_mostrar}"
        if self.modified:
            titulo += " *"
        self.root.title(titulo)

    def on_text_modified(self, event=None):
        if self.code_text.edit_modified():
            self.modified = True
            self.update_title()
            self.code_text.edit_modified(False)

    def nuevo_archivo(self):
        if self.modified:
            respuesta = messagebox.askyesnocancel("Guardar cambios", "¿Desea guardar los cambios antes de crear un nuevo archivo?")
            if respuesta is True:
                self.guardar_archivo()
            elif respuesta is None:
                return

        self.code_text.delete("1.0", tk.END)
        self.result_text.delete("1.0", tk.END)
        self.current_file = None
        self.modified = False
        self.code_text.config(state=tk.NORMAL)
        self.update_title()  # Título actualizado
        self.status_bar.config(text="Archivo: Ninguno")

    def abrir_archivo(self):
        if self.modified:
            respuesta = messagebox.askyesnocancel("Guardar cambios", "¿Desea guardar los cambios?")
            if respuesta is True:
                self.guardar_archivo()
            elif respuesta is None:
                return

        file_path = filedialog.askopenfilename(
            title="Abrir archivo MicroC",
            filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.code_text.delete("1.0", tk.END)
            self.code_text.insert("1.0", contenido)
            self.current_file = file_path
            self.modified = False
            self.code_text.config(state=tk.DISABLED)
            self.update_title()  # Título con ruta completa
            self.status_bar.config(text=f"Archivo: {file_path}")
            self.result_text.insert(tk.END, f"Archivo cargado: {file_path}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar_archivo(self):
        contenido = self.code_text.get("1.0", tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay nada que guardar.")
            return

        if self.current_file is None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".c",
                filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
            )
            if not file_path:
                return
            self.current_file = file_path
        else:
            file_path = self.current_file

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(contenido)
            self.modified = False
            self.update_title()  # Título actualizado
            self.status_bar.config(text=f"Archivo: {file_path}")
            self.result_text.insert(tk.END, f"Archivo guardado: {file_path}\n")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def salir(self):
        if self.modified:
            respuesta = messagebox.askyesnocancel("Guardar cambios", "Hay cambios sin guardar. ¿Desea guardarlos antes de salir?")
            if respuesta is True:
                self.guardar_archivo()
                if self.modified:
                    return
            elif respuesta is None:
                return
        self.root.quit()

    def editar(self):
        self.code_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, "Modo edición activado.\n")

    def compilar(self):
        contenido = self.code_text.get("1.0", tk.END).strip()
        if not contenido:
            messagebox.showwarning("Advertencia", "No hay código para compilar.")
            return
        self.result_text.insert(tk.END, "Compilación en proceso.\n")

    def ayuda(self):
        messagebox.showinfo("Ayuda", "Pre compilador\n\n"
                            "Funciones:\n"
                            "- Nuevo: crear archivo vacío\n"
                            "- Abrir: cargar archivo .C (solo lectura)\n"
                            "- Guardar: guardar cambios\n"
                            "- Editar: habilitar edición\n"
                            "- Compilar: simulación\n"
                            "- Salir: cerrar aplicación")

if __name__ == "__main__":
    root = tk.Tk()
    app = Pre_compilador(root)
    root.mainloop()