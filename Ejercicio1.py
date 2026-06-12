import tkinter as tk


class VentanaInfo(tk.Toplevel):
    #Ventana secundaria que muestra un mensaje centrado.

    def __init__(self, root, texto, nombre):
        super().__init__(root)
        self.title(nombre)
        self.geometry("250x100")
        self.maxsize(250, 100)
        self.minsize(250, 100)
        tk.Label(self, text=texto, font=("Arial", 14)).place(
            relx=0.5, rely=0.5, anchor="center"
        )
        root.withdraw()


class AppDivision(tk.Tk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        self.title("División")
        self.geometry("300x150")
        self.minsize(300, 150)
        self.maxsize(300, 150)
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(self, text="Numerador: ", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=2
        )
        tk.Label(self, text="Denominador: ", font=("Arial", 14)).grid(
            row=1, column=0, columnspan=2
        )
        tk.Button(
            self, text="Calcular", command=self.prueba_excepciones, font=("Arial", 14)
        ).grid(row=3, column=0, columnspan=2)

        self.msg = tk.Label(self, text="", font=("Arial", 14), fg="red")
        self.msg.place(relx=0.5, rely=0.7, anchor="center")

        self.entrada1 = tk.Entry(self)
        self.entrada2 = tk.Entry(self)
        self.entrada1.grid(row=0, column=2, columnspan=2)
        self.entrada2.grid(row=1, column=2, columnspan=2)

    def crear_ventana_info(self, texto, nombre):
        return VentanaInfo(self, texto, nombre)

    def prueba_excepciones(self):
        entradas = [self.entrada1, self.entrada2]
        numeros = []
        for e in entradas:
            try:
                numeros.append(float(e.get()))
            except ValueError:
                self.msg.config(text="Por favor ingrese numeros")
                return
        self.msg.config(text="")

        try:
            ventana1 = self.crear_ventana_info("Ingresando al primer try", "Primer try")
            cociente = numeros[0] / numeros[1]

            def exito_division():
                ventana1.destroy()
                ventana_despues = self.crear_ventana_info(
                    "Después de la división", "Después de division"
                )
                self.after(
                    1500,
                    lambda: (
                        ventana_despues.destroy(),
                        self.segundo_bloque_try(cociente),
                    ),
                )

            self.after(1500, exito_division)

        except ZeroDivisionError:
            def error_division():
                ventana1.destroy()
                ventana_error = self.crear_ventana_info("División por cero", "Error")
                self.after(
                    1500,
                    lambda: (
                        ventana_error.destroy(),
                        self.segundo_bloque_try(None),
                    ),
                )

            self.after(1500, error_division)

    def segundo_bloque_try(self, resultado_primer_try):
        ventana2 = self.crear_ventana_info("Ingresando al segundo try", "Segundo try")

        def evaluar_segundo_bloque():
            try:
                resultado_primer_try.split()  # falla siempre (float o None)
                ventana2.destroy()
                ventana_obj = self.crear_ventana_info("Imprimiendo resultado", "Resultado")
                self.after(1500, lambda: self.final_de_flujo(ventana_obj, resultado_primer_try))

            except ZeroDivisionError:
                ventana2.destroy()
                ventana_zero = self.crear_ventana_info("División por cero", "Error")
                self.after(1500, lambda: self.final_de_flujo(ventana_zero, resultado_primer_try))

            except Exception:
                ventana2.destroy()
                ventana_gen = self.crear_ventana_info("Ocurrió una excepción", "Excepción")
                self.after(1500, lambda: self.final_de_flujo(ventana_gen, resultado_primer_try))

        self.after(1500, evaluar_segundo_bloque)

    def final_de_flujo(self, ventana_anterior, resultado):
        ventana_anterior.destroy()
        self.deiconify()
        if resultado is not None:
            self.msg.config(text=f"Resultado: {resultado:.2f}", fg="black")
        else:
            self.msg.config(text="División por cero", fg="red")


if __name__ == "__main__":
    app = AppDivision()
    app.mainloop()