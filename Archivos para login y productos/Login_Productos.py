import tkinter as tk
from tkinter import messagebox, Menu, filedialog
import json # Para guardar y cargar datos de productos de forma estructurada

# --- Configuración de Archivos ---
USER_DATA_FILE = "user_data.txt"
PRODUCT_DATA_FILE = "product_data.json" # Archivo para guardar los productos

# --- Funciones de Gestión de Usuarios ---
def load_users():
    """Carga los usuarios y contraseñas desde el archivo."""
    users = {}
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                username, password = line.strip().split(":")
                users[username] = password
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    """Guarda los usuarios y contraseñas en el archivo."""
    with open(USER_DATA_FILE, "w") as f:
        for username, password in users.items():
            f.write(f"{username}:{password}\n")

# --- Clase para la Aplicación de Productos ---
class ProductApp:
    def __init__(self, master):
        self.master = master
        master.title("Gestión de Productos")
        master.geometry("450x400")

        self.products = [] # Lista para almacenar todos los productos

        self.create_widgets()
        self.create_menu()
        self.load_products() # Cargar productos al iniciar la aplicación

    def create_widgets(self):
        # Frame para los campos de entrada
        input_frame = tk.Frame(self.master, padx=10, pady=10)
        input_frame.pack(fill="both", expand=True)

        # Fecha
        tk.Label(input_frame, text="Fecha (DD/MM/AAAA):").grid(row=0, column=0, sticky="w", pady=5)
        self.fecha_entry = tk.Entry(input_frame, width=30)
        self.fecha_entry.grid(row=0, column=1, pady=5)

        # Nombre del Producto
        tk.Label(input_frame, text="Nombre del Producto:").grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_producto_entry = tk.Entry(input_frame, width=30)
        self.nombre_producto_entry.grid(row=1, column=1, pady=5)

        # Cantidad del Producto
        tk.Label(input_frame, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=5)
        self.cantidad_entry = tk.Entry(input_frame, width=30)
        self.cantidad_entry.grid(row=2, column=1, pady=5)
        self.cantidad_entry.bind("<KeyRelease>", self.calculate_total) # Calcular al escribir

        # Unidad Unitaria (Precio por unidad)
        tk.Label(input_frame, text="Precio Unitario:").grid(row=3, column=0, sticky="w", pady=5)
        self.precio_unitario_entry = tk.Entry(input_frame, width=30)
        self.precio_unitario_entry.grid(row=3, column=1, pady=5)
        self.precio_unitario_entry.bind("<KeyRelease>", self.calculate_total) # Calcular al escribir

        # Total
        tk.Label(input_frame, text="Total:").grid(row=4, column=0, sticky="w", pady=5)
        self.total_label = tk.Label(input_frame, text="0.00", font=("Arial", 12, "bold"))
        self.total_label.grid(row=4, column=1, sticky="w", pady=5)

        # Botón para agregar/guardar el producto actual
        self.add_product_button = tk.Button(input_frame, text="Guardar Producto Actual", command=self.save_current_product)
        self.add_product_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Área para mostrar la lista de productos (opcional, para visualización)
        tk.Label(self.master, text="Productos Guardados:").pack(pady=5)
        self.product_list_text = tk.Text(self.master, height=8, width=50, state="disabled")
        self.product_list_text.pack(pady=5)
        self.update_product_list_display()

    def create_menu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # Menú Archivo
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.load_products_from_file) # Abre un diálogo para seleccionar archivo
        file_menu.add_command(label="Guardar", command=self.save_products_to_file) # Guarda todos los productos en un archivo
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.quit)

        # Menú Opciones
        options_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=options_menu)
        options_menu.add_command(label="Agregar otro producto", command=self.clear_fields)

    def calculate_total(self, event=None):
        try:
            cantidad = float(self.cantidad_entry.get() or 0)
            precio_unitario = float(self.precio_unitario_entry.get() or 0)
            total = cantidad * precio_unitario
            self.total_label.config(text=f"{total:.2f}")
        except ValueError:
            self.total_label.config(text="Error")

    def clear_fields(self):
        """Limpia todos los campos de entrada para agregar un nuevo producto."""
        self.fecha_entry.delete(0, tk.END)
        self.nombre_producto_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.precio_unitario_entry.delete(0, tk.END)
        self.total_label.config(text="0.00")
        messagebox.showinfo("Nuevo Producto", "Campos limpiados para agregar un nuevo producto.")

    def save_current_product(self):
        """Guarda el producto que está actualmente en los campos de entrada."""
        fecha = self.fecha_entry.get()
        nombre = self.nombre_producto_entry.get()
        cantidad_str = self.cantidad_entry.get()
        precio_str = self.precio_unitario_entry.get()
        total_str = self.total_label.cget("text")

        if not all([fecha, nombre, cantidad_str, precio_str]):
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos del producto.")
            return

        try:
            cantidad = float(cantidad_str)
            precio_unitario = float(precio_str)
            total = float(total_str)
        except ValueError:
            messagebox.showerror("Error de Datos", "Cantidad y Precio Unitario deben ser números válidos.")
            return

        product = {
            "fecha": fecha,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total
        }
        self.products.append(product)
        self.update_product_list_display()
        messagebox.showinfo("Producto Guardado", "Producto actual guardado en la lista.")
        self.clear_fields() # Limpiar campos después de guardar

    def update_product_list_display(self):
        """Actualiza el área de texto para mostrar los productos guardados."""
        self.product_list_text.config(state="normal")
        self.product_list_text.delete("1.0", tk.END)
        if self.products:
            for i, product in enumerate(self.products):
                self.product_list_text.insert(tk.END, f"Producto {i+1}:\n")
                self.product_list_text.insert(tk.END, f"  Fecha: {product['fecha']}\n")
                self.product_list_text.insert(tk.END, f"  Nombre: {product['nombre']}\n")
                self.product_list_text.insert(tk.END, f"  Cantidad: {product['cantidad']}\n")
                self.product_list_text.insert(tk.END, f"  Precio Unitario: {product['precio_unitario']:.2f}\n")
                self.product_list_text.insert(tk.END, f"  Total: {product['total']:.2f}\n\n")
        else:
            self.product_list_text.insert(tk.END, "No hay productos guardados aún.")
        self.product_list_text.config(state="disabled")

    def save_products_to_file(self):
        """Guarda todos los productos en un archivo JSON."""
        try:
            with open(PRODUCT_DATA_FILE, "w") as f:
                json.dump(self.products, f, indent=4)
            messagebox.showinfo("Guardar Productos", f"Productos guardados en '{PRODUCT_DATA_FILE}'.")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar los productos: {e}")

    def load_products(self):
        """Carga los productos desde el archivo JSON al iniciar la aplicación."""
        try:
            with open(PRODUCT_DATA_FILE, "r") as f:
                self.products = json.load(f)
            self.update_product_list_display()
            messagebox.showinfo("Cargar Productos", f"Productos cargados desde '{PRODUCT_DATA_FILE}'.")
        except FileNotFoundError:
            messagebox.showinfo("Cargar Productos", "No se encontró el archivo de productos. Se creará uno nuevo al guardar.")
        except json.JSONDecodeError:
            messagebox.showerror("Error al Cargar", "El archivo de productos está corrupto o vacío. Se iniciará con una lista vacía.")
            self.products = [] # Reiniciar si el archivo está corrupto
        except Exception as e:
            messagebox.showerror("Error al Cargar", f"Ocurrió un error al cargar los productos: {e}")

    def load_products_from_file(self):
        """Permite al usuario seleccionar un archivo JSON para cargar productos."""
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r") as f:
                loaded_products = json.load(f)
            self.products = loaded_products
            self.update_product_list_display()
            messagebox.showinfo("Cargar Productos", f"Productos cargados desde '{filepath}'.")
        except FileNotFoundError:
            messagebox.showerror("Error al Cargar", "El archivo seleccionado no existe.")
        except json.JSONDecodeError:
            messagebox.showerror("Error al Cargar", "El archivo seleccionado no es un JSON válido o está vacío.")
        except Exception as e:
            messagebox.showerror("Error al Cargar", f"Ocurrió un error al cargar el archivo: {e}")


# --- Clase para la Aplicación de Login/Registro ---
class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Inicio de Sesión y Registro")
        master.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        username_label = tk.Label(self.master, text="Usuario:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.master, text="Contraseña:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.master, text="Iniciar Sesión", command=self.login)
        login_button.pack(pady=5)

        register_button = tk.Button(self.master, text="Registrarse", command=self.register)
        register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = load_users()

        if username in users and users[username] == password:
            messagebox.showinfo("Inicio de Sesión Exitoso", f"¡Bienvenido, {username}!")
            self.master.destroy() # Cierra la ventana de login
            self.open_product_app() # Abre la aplicación de productos
        else:
            messagebox.showerror("Error de Inicio de Sesión", "Nombre de usuario o contraseña incorrectos.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = load_users()

        if not username or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingresa un nombre de usuario y una contraseña.")
            return

        if username in users:
            messagebox.showerror("Error de Registro", "El nombre de usuario ya existe. Por favor, elige otro.")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Registro Exitoso", f"Usuario '{username}' registrado correctamente. ¡Ya puedes iniciar sesión!")

    def open_product_app(self):
        product_root = tk.Tk()
        product_app = ProductApp(product_root)
        product_root.mainloop()

# --- Ejecución Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()