import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import subprocess
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def verificar_pin_windows_nativo():
    """
    Abre de forma segura el cuadro oficial de Windows Hello/PIN utilizando 
    un comando de autenticación directa del sistema operativo.
    """
    current_user = os.getlogin()
    
    script_prompt = f"""
    $cred = Get-Credential -UserName "{current_user}" -Message "Confirme su PIN o credencial de Windows para ingresar."
    if ($cred) {{
        exit 0
    }} else {{
        exit 1
    }}
    """
    
    try:
        resultado = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script_prompt],
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
            capture_output=True,
            text=True
        )
        
        if resultado.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

# Inicializar Base de Datos SQLite
def init_db():
    conn = sqlite3.connect("finanzas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            tipo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class AppFinanzas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Autenticación - Finanzas Personales")
        self.geometry("900x600")
        self.resizable(False, False)
        
        self.current_user = None
        self.mostrar_ventana_login()

    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_ventana_login(self):
        self.limpiar_ventana()

        frame_login = ctk.CTkFrame(self, width=450, height=500, corner_radius=15)
        frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        lbl_titulo = ctk.CTkLabel(frame_login, text="Finanzas Personales", font=("Arial", 24, "bold"))
        lbl_titulo.pack(pady=25)

        lbl_sub = ctk.CTkLabel(frame_login, text="Inicie sesión o cree una cuenta para continuar", font=("Arial", 12), text_color="gray")
        lbl_sub.pack(pady=5)

        # Pestañas lógicas
        self.tab_view = ctk.CTkTabview(frame_login, width=380, height=340)
        self.tab_view.pack(pady=10)
        
        tab_win = self.tab_view.add("Windows Hello / PIN")
        tab_trad = self.tab_view.add("Cuenta Tradicional")

        # --- Pestaña Windows Hello / Sistema ---
        lbl_win_info = ctk.CTkLabel(tab_win, text=f"Usuario de Windows:\n{os.getlogin()}", font=("Arial", 14, "bold"), text_color="#2ecc71")
        lbl_win_info.pack(pady=20)

        btn_windows_hello = ctk.CTkButton(
            tab_win, 
            text="Validar con PIN / Windows Hello", 
            command=self.autenticar_windows_hello,
            fg_color="#27ae60", 
            hover_color="#219653",
            height=45,
            font=("Arial", 13, "bold")
        )
        btn_windows_hello.pack(pady=20, fill=tk.X, padx=20)

        lbl_win_desc = ctk.CTkLabel(tab_win, text="Utiliza el PIN o contraseña de tu equipo para ingresar al instante.", font=("Arial", 10), text_color="gray", wraplength=300)
        lbl_win_desc.pack(pady=10)

        # --- Pestaña Tradicional (Usuario / Contraseña) ---
        self.entry_user_trad = ctk.CTkEntry(tab_trad, placeholder_text="Usuario", width=280, height=38)
        self.entry_user_trad.pack(pady=15)

        self.entry_pass_trad = ctk.CTkEntry(tab_trad, placeholder_text="Contraseña", show="*", width=280, height=38)
        self.entry_pass_trad.pack(pady=15)

        btn_login_trad = ctk.CTkButton(tab_trad, text="Iniciar Sesión", command=self.login_tradicional, width=280, height=38)
        btn_login_trad.pack(pady=10)

        btn_registro_trad = ctk.CTkButton(tab_trad, text="Registrar Nueva Cuenta", command=self.registrar_tradicional, fg_color="#34495e", hover_color="#2c3e50", width=280, height=38)
        btn_registro_trad.pack(pady=5)

    def autenticar_windows_hello(self):
        self.withdraw()
        
        exito = verificar_pin_windows_nativo()
        
        if exito:
            self.current_user = os.getlogin()
            self.mostrar_dashboard()
        else:
            self.deiconify()

    def login_tradicional(self):
        user = self.entry_user_trad.get().strip()
        pwd = self.entry_pass_trad.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return

        conn = sqlite3.connect("finanzas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (user, pwd))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            self.current_user = user
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")

    def registrar_tradicional(self):
        user = self.entry_user_trad.get().strip()
        pwd = self.entry_pass_trad.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos Vacíos", "Ingrese usuario y contraseña para registrarse.")
            return

        try:
            conn = sqlite3.connect("finanzas.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cuenta registrada correctamente. Ya puede iniciar sesión.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe en el sistema.")

    def mostrar_dashboard(self):
        self.deiconify()
        self.limpiar_ventana()

        # Barra Superior
        top_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        top_bar.pack(fill=tk.X, side=tk.TOP)

        lbl_welcome = ctk.CTkLabel(top_bar, text=f"Bienvenido, {self.current_user}", font=("Arial", 16, "bold"))
        lbl_welcome.pack(side=tk.LEFT, padx=20)

        btn_logout = ctk.CTkButton(top_bar, text="Cerrar Sesión", command=self.mostrar_ventana_login, fg_color="#c0392b", hover_color="#962d22", width=100)
        btn_logout.pack(side=tk.RIGHT, padx=20)

        # Contenedor Principal Dashboard
        main_content = ctk.CTkFrame(self, fg_color="transparent")
        main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Formulario para agregar transacciones
        form_frame = ctk.CTkFrame(main_content, width=300)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        lbl_trans = ctk.CTkLabel(form_frame, text="Nueva Transacción", font=("Arial", 14, "bold"))
        lbl_trans.pack(pady=15)

        self.tipo_var = ctk.StringVar(value="Ingreso")
        cb_tipo = ctk.CTkComboBox(form_frame, values=["Ingreso", "Gasto"], variable=self.tipo_var, width=220)
        cb_tipo.pack(pady=10)

        self.entry_cat = ctk.CTkEntry(form_frame, placeholder_text="Categoría (ej. Comida)", width=220)
        self.entry_cat.pack(pady=10)

        self.entry_monto = ctk.CTkEntry(form_frame, placeholder_text="Monto", width=220)
        self.entry_monto.pack(pady=10)

        btn_agregar = ctk.CTkButton(form_frame, text="Guardar Transacción", command=self.agregar_transaccion, width=220, fg_color="#27ae60", hover_color="#219653")
        btn_agregar.pack(pady=20)

        # Contenedor de Gráficos Matplotlib
        self.graph_frame = ctk.CTkFrame(main_content)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.actualizar_grafico()

    def agregar_transaccion(self):
        tipo = self.tipo_var.get()
        categoria = self.entry_cat.get().strip()
        monto_str = self.entry_monto.get().strip()

        if not categoria or not monto_str:
            messagebox.showwarning("Advertencia", "Rellene todos los campos.")
            return

        try:
            monto = float(monto_str)
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número válido.")
            return

        conn = sqlite3.connect("finanzas.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transacciones (username, tipo, categoria, monto, fecha) VALUES (?, ?, ?, ?, datetime('now'))",
                       (self.current_user, tipo, categoria, monto))
        conn.commit()
        conn.close()

        self.entry_cat.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.actualizar_grafico()

    def actualizar_grafico(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("finanzas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tipo, SUM(monto) FROM transacciones WHERE username = ? GROUP BY tipo", (self.current_user,))
        datos = cursor.fetchall()
        conn.close()

        fig, ax = plt.subplots(figsize=(5, 4))
        if datos:
            tipos = [d[0] for d in datos]
            montos = [d[1] for d in datos]
            ax.bar(tipos, montos, color=['#27ae60', '#c0392b'])
            ax.set_title("Balance General")
            ax.set_ylabel("Monto")
        else:
            ax.text(0.5, 0.5, "Sin transacciones registradas", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.set_axis_off()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()