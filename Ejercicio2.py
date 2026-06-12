import tkinter as tk


class IllegalArgumentException(Exception):
    #Excepción personalizada equivalente a IllegalArgumentException de Java
    pass


class Vendedor:

    def __init__(self, nombre, apellidos, edad):
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = self.verificar_edad(edad)

    def verificar_edad(self, edad):
        if edad < 0 or edad > 120:
            raise IllegalArgumentException("La edad no puede ser negativa ni mayor a 120")
        if edad <= 18:
            raise IllegalArgumentException("El vendedor debe ser mayor de 18 años")
        return edad

    def imprimir(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"Apellidos: {self.apellidos}\n"
            f"Edad: {self.edad}"
        )


class VentanaInfo(tk.Toplevel):
    #Ventana secundaria que muestra un mensaje centrado

    def __init__(self, root, texto, nombre):
        super().__init__(root)
        self.title(nombre)
        self.geometry("320x100")
        self.maxsize(320, 100)
        self.minsize(320, 100)
        self.resizable(False, False)
        tk.Label(self, text=texto, font=("Arial", 12), wraplength=300).place(
            relx=0.5, rely=0.5, anchor="center"
        )
        root.withdraw()


class AppVendedor(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Registro de Vendedor")
        self.geometry("350x220")
        self.minsize(350, 220)
        self.maxsize(350, 220)
        self.resizable(False, False)
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(self, text="Nombre:", font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=8, sticky="e"
        )
        tk.Label(self, text="Apellidos:", font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=8, sticky="e"
        )
        tk.Label(self, text="Edad:", font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=8, sticky="e"
        )

        self.entrada_nombre = tk.Entry(self, font=("Arial", 12))
        self.entrada_apellidos = tk.Entry(self, font=("Arial", 12))
        self.entrada_edad = tk.Entry(self, font=("Arial", 12))

        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=8)
        self.entrada_apellidos.grid(row=1, column=1, padx=10, pady=8)
        self.entrada_edad.grid(row=2, column=1, padx=10, pady=8)

        tk.Button(
            self, text="Registrar", command=self.registrar_vendedor, font=("Arial", 12)
        ).grid(row=3, column=0, columnspan=2, pady=10)

        self.msg = tk.Label(self, text="", font=("Arial", 11), fg="red", wraplength=330)
        self.msg.grid(row=4, column=0, columnspan=2)

    def crear_ventana_info(self, texto, nombre):
        return VentanaInfo(self, texto, nombre)

    def registrar_vendedor(self):
        nombre = self.entrada_nombre.get().strip()
        apellidos = self.entrada_apellidos.get().strip()
        edad_str = self.entrada_edad.get().strip()

        if not nombre or not apellidos or not edad_str:
            self.msg.config(text="Por favor complete todos los campos", fg="red")
            return

        try:
            edad = int(edad_str)
        except ValueError:
            self.msg.config(text="La edad debe ser un número entero", fg="red")
            return

        self.msg.config(text="")

        try:
            ventana1 = self.crear_ventana_info("Verificando datos del vendedor...", "Verificando")
            vendedor = Vendedor(nombre, apellidos, edad)

            def mostrar_exito():
                ventana1.destroy()
                ventana_ok = self.crear_ventana_info("Vendedor registrado con éxito", "Éxito")
                self.after(1500, lambda: self.mostrar_resultado(ventana_ok, vendedor))

            self.after(1500, mostrar_exito)

        except IllegalArgumentException as e:
            mensaje_error = str(e)  # capturar antes de que Python elimine 'e' del scope
            def mostrar_error():
                ventana1.destroy()
                ventana_err = self.crear_ventana_info(mensaje_error, "Error")
                self.after(1500, lambda: self.final_de_flujo(ventana_err, None))

            self.after(1500, mostrar_error)

        except Exception:
            def mostrar_excepcion():
                ventana1.destroy()
                ventana_gen = self.crear_ventana_info("Ocurrió una excepción inesperada", "Excepción")
                self.after(1500, lambda: self.final_de_flujo(ventana_gen, None))

            self.after(1500, mostrar_excepcion)

    def mostrar_resultado(self, ventana_anterior, vendedor):
        ventana_anterior.destroy()
        ventana_datos = self.crear_ventana_info(vendedor.imprimir(), "Datos del Vendedor")
        self.after(2500, lambda: self.final_de_flujo(ventana_datos, vendedor))

    def final_de_flujo(self, ventana_anterior, vendedor):
        ventana_anterior.destroy()
        self.deiconify()
        if vendedor is not None:
            self.msg.config(
                text=f"{vendedor.nombre} {vendedor.apellidos} registrado correctamente",
                fg="green"
            )
        else:
            self.msg.config(text="No se pudo registrar el vendedor", fg="red")


if __name__ == "__main__":
    app = AppVendedor()
    app.mainloop()