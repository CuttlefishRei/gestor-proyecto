import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import autenticador

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def init_db():
    conn = sqlite3.connect("finanzas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            usa_windows_hello INTEGER DEFAULT 0
        )
    """)
    
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN usa_windows_hello INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

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
        self.title("Finanzas Personales - Panel Avanzado")
        self.geometry("1100x700")
        self.resizable(False, False)
        
        self.current_user = None
        self.mostrar_ventana_login()

    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_ventana_login(self):
        self.limpiar_ventana()

        frame_login = ctk.CTkFrame(self, width=460, height=520, corner_radius=20)
        frame_login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        lbl_titulo = ctk.CTkLabel(frame_login, text="Finanzas Personales", font=("Arial", 26, "bold"))
        lbl_titulo.pack(pady=30)

        sys_user = os.getlogin()
        conn = sqlite3.connect("finanzas.db")
        cursor = conn.cursor()
        cursor.execute("SELECT usa_windows_hello FROM usuarios WHERE usa_windows_hello = 1")
        res = cursor.fetchone()
        conn.close()
        
        tiene_hello_activado = res is not None

        if tiene_hello_activado:
            lbl_sub = ctk.CTkLabel(frame_login, text=f"Acceso rápido disponible para: {sys_user}", font=("Arial", 12), text_color="#2ecc71")
            lbl_sub.pack(pady=5)

            btn_hello = ctk.CTkButton(
                frame_login, 
                text="🛡️ Entrar con Windows Hello / PIN", 
                command=self.login_con_windows_hello,
                fg_color="#27ae60", hover_color="#219653",
                height=45, width=320, font=("Arial", 14, "bold")
            )
            btn_hello.pack(pady=20)

            lbl_o = ctk.CTkLabel(frame_login, text="--- O usa tu cuenta tradicional ---", font=("Arial", 10), text_color="gray")
            lbl_o.pack(pady=5)

        self.tab_view = ctk.CTkTabview(frame_login, width=400, height=280)
        self.tab_view.pack(pady=10)
        
        tab_trad = self.tab_view.add("Cuenta Tradicional")

        self.entry_user_trad = ctk.CTkEntry(tab_trad, placeholder_text="Usuario", width=300, height=40)
        self.entry_user_trad.pack(pady=15)

        self.entry_pass_trad = ctk.CTkEntry(tab_trad, placeholder_text="Contraseña", show="*", width=300, height=40)
        self.entry_pass_trad.pack(pady=10)

        btn_login_trad = ctk.CTkButton(tab_trad, text="Iniciar Sesión", command=self.login_tradicional, width=300, height=40)
        btn_login_trad.pack(pady=10)

        btn_registro_trad = ctk.CTkButton(tab_trad, text="Registrar Cuenta", command=self.registrar_tradicional, fg_color="#34495e", hover_color="#2c3e50", width=300, height=40)
        btn_registro_trad.pack(pady=5)

    def login_con_windows_hello(self):
        if autenticador.verificar_pin_sistema():
            conn = sqlite3.connect("finanzas.db")
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM usuarios WHERE usa_windows_hello = 1 LIMIT 1")
            res = cursor.fetchone()
            conn.close()
            
            self.current_user = res[0] if res else os.getlogin()
            self.mostrar_dashboard()
        else:
            messagebox.showwarning("Acceso Denegado", "No se completó la verificación del sistema.")

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
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar_tradicional(self):
        user = self.entry_user_trad.get().strip()
        pwd = self.entry_pass_trad.get().strip()

        if not user or not pwd:
            messagebox.showwarning("Campos Vacíos", "Ingrese usuario y contraseña para registrarse.")
            return

        try:
            conn = sqlite3.connect("finanzas.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password, usa_windows_hello) VALUES (?, ?, 0)", (user, pwd))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Cuenta registrada correctamente.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")

    def mostrar_dashboard(self):
        self.limpiar_ventana()

        top_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        top_bar.pack(fill=tk.X, side=tk.TOP)

        lbl_welcome = ctk.CTkLabel(top_bar, text=f"Panel Financiero | Usuario: {self.current_user}", font=("Arial", 16, "bold"))
        lbl_welcome.pack(side=tk.LEFT, padx=20)

        btn_vincular = ctk.CTkButton(top_bar, text="🛡️ Activar Windows Hello", command=self.activar_windows_hello_usuario, fg_color="#27ae60", hover_color="#219653", width=160)
        btn_vincular.pack(side=tk.LEFT, padx=10)

        btn_logout = ctk.CTkButton(top_bar, text="Cerrar Sesión", command=self.mostrar_ventana_login, fg_color="#c0392b", hover_color="#962d22", width=110)
        btn_logout.pack(side=tk.RIGHT, padx=20)

        main_content = ctk.CTkFrame(self, fg_color="transparent")
        main_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Panel izquierdo para formularios
        form_frame = ctk.CTkFrame(main_content, width=300)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        lbl_trans = ctk.CTkLabel(form_frame, text="Gestión de Movimientos", font=("Arial", 15, "bold"))
        lbl_trans.pack(pady=15)

        self.tipo_var = ctk.StringVar(value="Ingreso")
        cb_tipo = ctk.CTkComboBox(form_frame, values=["Ingreso", "Gasto", "Deuda"], variable=self.tipo_var, width=250, height=35)
        cb_tipo.pack(pady=10)

        self.entry_cat = ctk.CTkEntry(form_frame, placeholder_text="Categoría (Ej. Comida / Préstamo)", width=250, height=35)
        self.entry_cat.pack(pady=10)

        self.entry_monto = ctk.CTkEntry(form_frame, placeholder_text="Monto ($)", width=250, height=35)
        self.entry_monto.pack(pady=10)

        btn_agregar = ctk.CTkButton(form_frame, text="Guardar Movimiento", command=self.agregar_transaccion, width=250, height=40, fg_color="#27ae60", hover_color="#219653")
        btn_agregar.pack(pady=20)

        # Panel derecho con Pestañas para las Gráficas
        self.tab_graficas = ctk.CTkTabview(main_content, width=720, height=580)
        self.tab_graficas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.tab_general = self.tab_graficas.add("Balance General")
        self.tab_pastel = self.tab_graficas.add("Desglose Gastos")
        self.tab_proyeccion = self.tab_graficas.add("Simulación Reducción")

        self.actualizar_graficas()

    def activar_windows_hello_usuario(self):
        if autenticador.verificar_pin_sistema():
            conn = sqlite3.connect("finanzas.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET usa_windows_hello = 1 WHERE username = ?", (self.current_user,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Seguridad Activada", "¡Listo! Windows Hello ha quedado habilitado para este equipo.")
        else:
            messagebox.showerror("Error", "No se pudo validar su identidad para activar Windows Hello.")

    def agregar_transaccion(self):
        tipo = self.tipo_var.get()
        categoria = self.entry_cat.get().strip()
        monto_str = self.entry_monto.get().strip()

        if not categoria or not monto_str:
            messagebox.showwarning("Advertencia", "Complete todos los campos.")
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
        self.actualizar_graficas()

    def actualizar_graficas(self):
        # Limpiar contenedores de pestañas
        for tab in [self.tab_general, self.tab_pastel, self.tab_proyeccion]:
            for widget in tab.winfo_children():
                widget.destroy()

        conn = sqlite3.connect("finanzas.db")
        cursor = conn.cursor()
        
        # 1. Datos para Balance General (Ingresos, Gastos, Deudas)
        cursor.execute("SELECT tipo, SUM(monto) FROM transacciones WHERE username = ? GROUP BY tipo", (self.current_user,))
        datos_totales = {fila[0]: fila[1] for fila in cursor.fetchall()}

        # 2. Datos para Desglose de Gastos por Categoría
        cursor.execute("SELECT categoria, SUM(monto) FROM transacciones WHERE username = ? AND tipo = 'Gasto' GROUP BY categoria", (self.current_user,))
        datos_gastos_cat = cursor.fetchall()

        conn.close()

        # --- GRÁFICA 1: Balance General (Barras) ---
        fig1, ax1 = plt.subplots(figsize=(6, 4.5))
        tipos = ['Ingreso', 'Gasto', 'Deuda']
        montos = [datos_totales.get('Ingreso', 0), datos_totales.get('Gasto', 0), datos_totales.get('Deuda', 0)]
        colores = ['#27ae60', '#c0392b', '#d35400']
        
        ax1.bar(tipos, montos, color=colores)
        ax1.set_title("Balance General (Ingresos vs Gastos vs Deudas)")
        ax1.set_ylabel("Monto ($)")
        
        canvas1 = FigureCanvasTkAgg(fig1, master=self.tab_general)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- GRÁFICA 2: Desglose de Gastos (Pastel) ---
        fig2, ax2 = plt.subplots(figsize=(6, 4.5))
        if datos_gastos_cat:
            cats = [d[0] for d in datos_gastos_cat]
            vals = [d[1] for d in datos_gastos_cat]
            ax2.pie(vals, labels=cats, autopct='%1.1f%%', startangle=140)
            ax2.set_title("Distribución Porcentual de Gastos")
        else:
            ax2.text(0.5, 0.5, "Sin gastos registrados", horizontalalignment='center', verticalalignment='center', transform=ax2.transAxes)
            ax2.set_axis_off()

        canvas2 = FigureCanvasTkAgg(fig2, master=self.tab_pastel)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- GRÁFICA 3: Simulación de Reducción (Comparativa Actual vs Reducido un 25%) ---
        fig3, ax3 = plt.subplots(figsize=(6, 4.5))
        gasto_actual = datos_totales.get('Gasto', 0)
        deuda_actual = datos_totales.get('Deuda', 0)
        
        # Simulamos una reducción óptima del 25% en gastos y deudas
        gasto_reducido = gasto_actual * 0.75
        deuda_reducida = deuda_actual * 0.75

        categorias_sim = ['Gastos Actuales', 'Gastos Reducidos', 'Deudas Actuales', 'Deudas Reducidas']
        valores_sim = [gasto_actual, gasto_reducido, deuda_actual, deuda_reducida]
        colores_sim = ['#e74c3c', '#2ecc71', '#e67e22', '#f39c12']

        ax3.bar(categorias_sim, valores_sim, color=colores_sim)
        ax3.set_title("Proyección con 25% de Reducción en Gastos y Deudas")
        ax3.set_ylabel("Monto ($)")
        plt.xticks(rotation=15)

        canvas3 = FigureCanvasTkAgg(fig3, master=self.tab_proyeccion)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()