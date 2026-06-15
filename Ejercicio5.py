import tkinter as tk
from tkinter import messagebox
import io


class LectorApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Lector de Archivos (Flujo de Bytes)")
        self.ventana.geometry("500x400")

        # Componentes de la interfaz
        self.boton_leer = tk.Button(
            self.ventana, text="Leer prueba.txt", command=self.procesar_archivo
        )
        self.boton_leer.pack(pady=10)

        self.area_texto = tk.Text(self.ventana, wrap="word")
        self.area_texto.pack(fill="both", expand=True, padx=10, pady=10)

    def procesar_archivo(self):
        # Limpia el área de texto antes de una nueva lectura
        self.area_texto.delete("1.0", tk.END)

        try:
            # Flujo de bytes (FileInputStream) encadenado al lector de caracteres (InputStreamReader)
            archivo_bytes = open("prueba.txt", "rb")
            lector = io.TextIOWrapper(archivo_bytes, encoding="utf-8")

            # Lectura línea a línea (BufferedReader) e inserción en la interfaz
            for linea in lector:
                self.area_texto.insert(tk.END, linea)

            lector.close()

        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo 'prueba.txt' no fue encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LectorApp(root)
    root.mainloop()
