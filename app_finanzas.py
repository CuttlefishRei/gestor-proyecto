import customtkinter as ctk
from autenticador import verificar_biometria_ltsc

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Base de datos simulada de usuarios y sus contraseñas
USUARIOS_REGISTRADOS = {"admin": "1234"}

# Almacén global de historiales por usuario para persistencia al cambiar de sesión
HISTORIALES_USUARIOS = {}

class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nexus Finance - Acceso")
        self.geometry("420x540")
        self.minsize(380, 480)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.usuario_actual = ""
        self.crear_interfaz_login()

    def limpiar_ventana(self):
        for widget in self.winfo_children():
            widget.destroy()

    def crear_interfaz_login(self):
        self.limpiar_ventana()

        card = ctk.CTkFrame(self, fg_color="#181920", corner_radius=20, border_width=1, border_color="#2b2d3d")
        card.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        card.grid_columnconfigure(0, weight=1)

        lbl_titulo = ctk.CTkLabel(card, text="NEXUS", font=("Segoe UI", 28, "bold"), text_color="#00f2fe")
        lbl_titulo.grid(row=0, column=0, pady=(35, 5))
        
        lbl_sub = ctk.CTkLabel(card, text="Tus finanzas inteligentes", font=("Segoe UI", 12), text_color="#8f93a2")
        lbl_sub.grid(row=1, column=0, pady=(0, 25))

        btn_biometrico = ctk.CTkButton(
            card, text="Acceso Biometrico", 
            fg_color="#00c6ff", hover_color="#008ecc", text_color="#0a0a0f",
            font=("Segoe UI", 13, "bold"), height=45, corner_radius=12,
            command=self.intentar_biometrico
        )
        btn_biometrico.grid(row=2, column=0, sticky="ew", padx=25, pady=10)

        lbl_o = ctk.CTkLabel(card, text="o inicia sesion de forma clasica", font=("Segoe UI", 11), text_color="#5c6070")
        lbl_o.grid(row=3, column=0, pady=8)

        self.entry_user = ctk.CTkEntry(card, placeholder_text="Usuario", height=42, corner_radius=10, fg_color="#101116", border_color="#2b2d3d")
        self.entry_user.grid(row=4, column=0, sticky="ew", padx=25, pady=6)

        self.entry_pass = ctk.CTkEntry(card, placeholder_text="Contrasena", show="*", height=42, corner_radius=10, fg_color="#101116", border_color="#2b2d3d")
        self.entry_pass.grid(row=5, column=0, sticky="ew", padx=25, pady=6)

        self.lbl_error = ctk.CTkLabel(card, text="", font=("Segoe UI", 11), text_color="#ff5e62")
        self.lbl_error.grid(row=6, column=0, pady=2)

        btn_login = ctk.CTkButton(
            card, text="Iniciar Sesion", 
            fg_color="#00f2fe", hover_color="#00c6ff", text_color="#0a0a0f",
            font=("Segoe UI", 14, "bold"), height=44, corner_radius=12,
            command=self.intentar_login_clasico
        )
        btn_login.grid(row=7, column=0, sticky="ew", padx=25, pady=10)

        btn_crear = ctk.CTkButton(
            card, text="Nuevo por aqui? Registrate", 
            fg_color="transparent", hover_color="#222431", 
            font=("Segoe UI", 12), text_color="#00f2fe",
            command=self.crear_interfaz_registro
        )
        btn_crear.grid(row=8, column=0, pady=(0, 20))

    def intentar_biometrico(self):
        if verificar_biometria_ltsc():
            self.usuario_actual = "Usuario Biometrico"
            self.abrir_dashboard()
        else:
            self.lbl_error.configure(text="Autenticacion biometrica cancelada.")

    def intentar_login_clasico(self):
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()

        if user in USUARIOS_REGISTRADOS and USUARIOS_REGISTRADOS[user] == pwd:
            self.usuario_actual = user
            self.abrir_dashboard()
        else:
            self.lbl_error.configure(text="Credenciales incorrectas.")

    def crear_interfaz_registro(self):
        self.limpiar_ventana()

        card = ctk.CTkFrame(self, fg_color="#181920", corner_radius=20, border_width=1, border_color="#2b2d3d")
        card.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        card.grid_columnconfigure(0, weight=1)

        lbl_titulo = ctk.CTkLabel(card, text="NUEVA CUENTA", font=("Segoe UI", 24, "bold"), text_color="#ff9900")
        lbl_titulo.grid(row=0, column=0, pady=(40, 25))

        self.reg_user = ctk.CTkEntry(card, placeholder_text="Elige un Usuario", height=42, corner_radius=10, fg_color="#101116", border_color="#2b2d3d")
        self.reg_user.grid(row=1, column=0, sticky="ew", padx=25, pady=8)

        self.reg_pass = ctk.CTkEntry(card, placeholder_text="Elige una Contrasena", show="*", height=42, corner_radius=10, fg_color="#101116", border_color="#2b2d3d")
        self.reg_pass.grid(row=2, column=0, sticky="ew", padx=25, pady=8)

        self.lbl_reg_error = ctk.CTkLabel(card, text="", font=("Segoe UI", 11), text_color="#ff5e62")
        self.lbl_reg_error.grid(row=3, column=0, pady=2)

        btn_registrar = ctk.CTkButton(
            card, text="Crear Cuenta", 
            fg_color="#ff9900", hover_color="#e08800", text_color="#0a0a0f",
            font=("Segoe UI", 14, "bold"), height=44, corner_radius=12,
            command=self.guardar_nuevo_usuario
        )
        btn_registrar.grid(row=4, column=0, sticky="ew", padx=25, pady=15)

        btn_volver = ctk.CTkButton(
            card, text="Volver al Login", 
            fg_color="transparent", hover_color="#222431", 
            font=("Segoe UI", 12), text_color="#8f93a2",
            command=self.crear_interfaz_login
        )
        btn_volver.grid(row=5, column=0, pady=(0, 20))

    def guardar_nuevo_usuario(self):
        user = self.reg_user.get().strip()
        pwd = self.reg_pass.get().strip()

        if not user or not pwd:
            self.lbl_reg_error.configure(text="Rellena todos los campos.")
            return

        if user in USUARIOS_REGISTRADOS:
            self.lbl_reg_error.configure(text="El usuario ya existe.")
            return

        USUARIOS_REGISTRADOS[user] = pwd
        self.crear_interfaz_login()

    def abrir_dashboard(self):
        self.destroy()
        app = DashboardFinanciero(self.usuario_actual)
        app.mainloop()


class DashboardFinanciero(ctk.CTk):
    def __init__(self, usuario):
        super().__init__()
        self.title("Nexus Finance - Dashboard")
        self.geometry("450x800")
        self.minsize(380, 650)
        self.usuario_activo = usuario

        # Totales reiniciados en cada inicio de sesión (gráfica limpia)
        self.total_ganancias = 0.0
        self.total_gastos = 0.0
        self.total_deudas = 0.0

        # Recuperar historial previo guardado para este usuario específico
        if self.usuario_activo not in HISTORIALES_USUARIOS:
            HISTORIALES_USUARIOS[self.usuario_activo] = []
        self.historial = HISTORIALES_USUARIOS[self.usuario_activo]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#0f1015")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.construir_dashboard()

    def construir_dashboard(self):
        # Cabecera moderna con saludo y botón de Cerrar Sesión
        header = ctk.CTkFrame(self.main_frame, fg_color="#181920", corner_radius=0, height=90)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        ctk.CTkLabel(header, text=f"Hola, {self.usuario_activo}", font=("Segoe UI", 18, "bold"), text_color="#00f2fe").grid(row=0, column=0, sticky="w", padx=20, pady=(15, 0))
        ctk.CTkLabel(header, text="Julio 2026 - Panel Financiero", font=("Segoe UI", 12), text_color="#8f93a2").grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

        # Botón de Cerrar Sesión
        btn_cerrar = ctk.CTkButton(
            header, text="Cerrar Sesion", 
            fg_color="#2b2d3d", hover_color="#ff5e62", text_color="white",
            font=("Segoe UI", 11, "bold"), height=30, width=100, corner_radius=8,
            command=self.cerrar_sesion
        )
        btn_cerrar.grid(row=0, column=1, rowspan=2, padx=20, sticky="e")

        # Botones de Acción Rápida
        acciones_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        acciones_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        acciones_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            acciones_frame, text="+ Ingreso", 
            fg_color="#00b09b", hover_color="#96c93d", text_color="#0a0a0f",
            font=("Segoe UI", 13, "bold"), height=42, corner_radius=12,
            command=lambda: self.abrir_ventana_transaccion("Ingreso")
        ).grid(row=0, column=0, sticky="ew", padx=5)

        ctk.CTkButton(
            acciones_frame, text="- Gasto", 
            fg_color="#ff5e62", hover_color="#ff9966", text_color="#0a0a0f",
            font=("Segoe UI", 13, "bold"), height=42, corner_radius=12,
            command=lambda: self.abrir_ventana_transaccion("Gasto")
        ).grid(row=0, column=1, sticky="ew", padx=5)

        ctk.CTkButton(
            self.main_frame, text="Registrar Deuda", 
            fg_color="#f7b733", hover_color="#fc4a1a", text_color="#0a0a0f",
            font=("Segoe UI", 13, "bold"), height=42, corner_radius=12,
            command=lambda: self.abrir_ventana_transaccion("Deuda")
        ).grid(row=2, column=0, sticky="ew", padx=20, pady=5)

        # Tarjeta Central con Gráfica de Anillos Estilizada
        card_grafico = ctk.CTkFrame(self.main_frame, fg_color="#181920", corner_radius=16, border_width=1, border_color="#2b2d3d")
        card_grafico.grid(row=3, column=0, sticky="ew", padx=20, pady=15)
        card_grafico.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card_grafico, text="Salud Financiera", font=("Segoe UI", 15, "bold"), text_color="white").grid(row=0, column=0, pady=(15, 5))

        self.canvas_grafico = ctk.CTkCanvas(card_grafico, width=170, height=170, bg="#181920", highlightthickness=0)
        self.canvas_grafico.grid(row=1, column=0, pady=10)
        self.dibujar_grafico(0, 0, 0)

        metrics_frame = ctk.CTkFrame(card_grafico, fg_color="transparent")
        metrics_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        metrics_frame.grid_columnconfigure((0, 1), weight=1)

        self.lbl_ganancias = ctk.CTkLabel(metrics_frame, text="Ingresos: $0.00", font=("Segoe UI", 12), text_color="#96c93d")
        self.lbl_ganancias.grid(row=0, column=0, sticky="w", pady=2)

        self.lbl_gastos = ctk.CTkLabel(metrics_frame, text="Gastos: $0.00", font=("Segoe UI", 12), text_color="#ff5e62")
        self.lbl_gastos.grid(row=0, column=1, sticky="w", pady=2)

        self.lbl_deudas = ctk.CTkLabel(metrics_frame, text="Deudas: $0.00", font=("Segoe UI", 12), text_color="#f7b733")
        self.lbl_deudas.grid(row=1, column=0, sticky="w", pady=2)

        self.lbl_balance = ctk.CTkLabel(card_grafico, text="Balance Neto: $0.00", font=("Segoe UI", 16, "bold"), text_color="#00f2fe")
        self.lbl_balance.grid(row=3, column=0, pady=(10, 20))

        # Sección de Historial de Transacciones del Mes
        ctk.CTkLabel(self.main_frame, text="Historial del Mes", font=("Segoe UI", 15, "bold"), text_color="white").grid(row=4, column=0, sticky="w", padx=25, pady=(10, 5))

        self.historial_frame = ctk.CTkFrame(self.main_frame, fg_color="#181920", corner_radius=16, border_width=1, border_color="#2b2d3d")
        self.historial_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.historial_frame.grid_columnconfigure(0, weight=1)

        self.actualizar_historial_ui()

    def cerrar_sesion(self):
        self.destroy()
        app = VentanaLogin()
        app.mainloop()

    def dibujar_grafico(self, g, gs, d):
        self.canvas_grafico.delete("all")
        total = g + gs + d

        if total == 0:
            self.canvas_grafico.create_oval(15, 15, 155, 155, outline="#2b2d3d", width=20)
            self.canvas_grafico.create_text(85, 85, text="Sin Registros", fill="#5c6070", font=("Segoe UI", 11, "bold"))
            return

        angulo_gs = (gs / total) * 360
        angulo_d = (d / total) * 360
        angulo_g = (g / total) * 360

        start = 0
        if gs > 0:
            self.canvas_grafico.create_arc(15, 15, 155, 155, start=start, extent=angulo_gs, style="arc", outline="#ff5e62", width=20)
            start += angulo_gs
        if d > 0:
            self.canvas_grafico.create_arc(15, 15, 155, 155, start=start, extent=angulo_d, style="arc", outline="#f7b733", width=20)
            start += angulo_d
        if g > 0:
            self.canvas_grafico.create_arc(15, 15, 155, 155, start=start, extent=angulo_g, style="arc", outline="#96c93d", width=20)

        self.canvas_grafico.create_text(85, 78, text="Balance", fill="#8f93a2", font=("Segoe UI", 10))
        neto = g - (gs + d)
        self.canvas_grafico.create_text(85, 98, text=f"${neto:.1f}", fill="#00f2fe", font=("Segoe UI", 13, "bold"))

    def abrir_ventana_transaccion(self, tipo):
        top = ctk.CTkToplevel(self)
        top.title(f"Nuevo {tipo}")
        top.geometry("340x350")
        top.resizable(False, False)
        top.grab_set()

        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top, text=f"Registrar {tipo}", font=("Segoe UI", 16, "bold"), text_color="#00f2fe").grid(row=0, column=0, pady=(20, 10))

        ctk.CTkLabel(top, text="Categoria:", font=("Segoe UI", 12), text_color="#8f93a2").grid(row=1, column=0, sticky="w", padx=35)
        
        categorias_opciones = {
            "Ingreso": ["Salario", "Freelance", "Inversiones", "Regalos", "Otros"],
            "Gasto": ["Comida / Super", "Transporte", "Servicios", "Entretenimiento", "Otros"],
            "Deuda": ["Prestamo Bancario", "Tarjeta de Credito", "Prestamo Personal", "Otros"]
        }

        combo_cat = ctk.CTkComboBox(top, values=categorias_opciones.get(tipo, ["General"]), width=260, height=38, fg_color="#181920", border_color="#2b2d3d")
        combo_cat.grid(row=2, column=0, pady=5)

        ctk.CTkLabel(top, text="Monto ($):", font=("Segoe UI", 12), text_color="#8f93a2").grid(row=3, column=0, sticky="w", padx=35)
        entry_monto = ctk.CTkEntry(top, placeholder_text="0.00", height=38, width=260, fg_color="#181920", border_color="#2b2d3d")
        entry_monto.grid(row=4, column=0, pady=5)

        lbl_msg = ctk.CTkLabel(top, text="", font=("Segoe UI", 11), text_color="#ff5e62")
        lbl_msg.grid(row=5, column=0)

        def guardar():
            try:
                valor = float(entry_monto.get().strip())
                if valor < 0:
                    raise ValueError()
                
                categoria = combo_cat.get()

                # Actualizar totales locales
                if tipo == "Ingreso":
                    self.total_ganancias += valor
                elif tipo == "Gasto":
                    self.total_gastos += valor
                elif tipo == "Deuda":
                    self.total_deudas += valor

                # Agregar al historial persistente del usuario
                self.historial.insert(0, {"tipo": tipo, "categoria": categoria, "monto": valor})

                self.actualizar_dashboard_ui()
                top.destroy()
            except ValueError:
                lbl_msg.configure(text="Ingresa un valor numerico valido.")

        btn_guardar = ctk.CTkButton(top, text="Guardar Movimiento", fg_color="#00f2fe", hover_color="#00c6ff", text_color="#0a0a0f", font=("Segoe UI", 14, "bold"), command=guardar, height=40, width=260)
        btn_guardar.grid(row=6, column=0, pady=15)

    def actualizar_dashboard_ui(self):
        self.lbl_ganancias.configure(text=f"Ingresos: ${self.total_ganancias:.2f}")
        self.lbl_gastos.configure(text=f"Gastos: ${self.total_gastos:.2f}")
        self.lbl_deudas.configure(text=f"Deudas: ${self.total_deudas:.2f}")

        balance_neto = self.total_ganancias - self.total_gastos - self.total_deudas
        self.lbl_balance.configure(text=f"Balance Neto: ${balance_neto:.2f}")
        
        if balance_neto >= 0:
            self.lbl_balance.configure(text_color="#00f2fe")
        else:
            self.lbl_balance.configure(text_color="#ff5e62")

        self.dibujar_grafico(self.total_ganancias, self.total_gastos, self.total_deudas)
        self.actualizar_historial_ui()

    def actualizar_historial_ui(self):
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        if not self.historial:
            lbl_vacio = ctk.CTkLabel(self.historial_frame, text="No hay movimientos registrados.", font=("Segoe UI", 12), text_color="#5c6070")
            lbl_vacio.pack(pady=15)
            return

        for item in self.historial:
            row = ctk.CTkFrame(self.historial_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=8)
            row.grid_columnconfigure(1, weight=1)

            color_tipo = "#96c93d" if item["tipo"] == "Ingreso" else ("#ff5e62" if item["tipo"] == "Gasto" else "#f7b733")
            simbolo = "+" if item["tipo"] == "Ingreso" else "-"

            lbl_icono = ctk.CTkLabel(row, text="o", font=("Segoe UI", 14), text_color=color_tipo)
            lbl_icono.grid(row=0, column=0, padx=(0, 8))

            lbl_info = ctk.CTkLabel(row, text=f"{item['tipo']} ({item['categoria']})", font=("Segoe UI", 12, "bold"), text_color="white")
            lbl_info.grid(row=0, column=1, sticky="w")

            lbl_monto = ctk.CTkLabel(row, text=f"{simbolo}${item['monto']:.2f}", font=("Segoe UI", 12, "bold"), text_color=color_tipo)
            lbl_monto.grid(row=0, column=2, sticky="e")


if __name__ == "__main__":
    app = VentanaLogin()
    app.mainloop()