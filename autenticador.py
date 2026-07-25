import ctypes

def verificar_pin_sistema():
    """Llama al diálogo nativo de credenciales de Windows usando ctypes."""
    try:
        class CREDUI_INFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("hwndParent", ctypes.c_void_p),
                ("pszMessageText", ctypes.c_wchar_p),
                ("pszCaptionText", ctypes.c_wchar_p),
                ("hbmBanner", ctypes.c_void_p),
            ]

        info = CREDUI_INFO()
        info.cbSize = ctypes.sizeof(CREDUI_INFO)
        info.hwndParent = None
        info.pszMessageText = "Por favor, introduce tu PIN o usa Windows Hello para continuar."
        info.pszCaptionText = "Seguridad de Finanzas Personales"

        auth_package = ctypes.c_ulong(0)
        out_auth_buffer = ctypes.c_void_p()
        out_auth_buffer_size = ctypes.c_ulong(0)
        f_save = ctypes.c_bool(False)

        resultado = ctypes.windll.credui.CredUIPromptForWindowsCredentialsW(
            ctypes.byref(info),
            0,
            ctypes.byref(auth_package),
            None,
            0,
            ctypes.byref(out_auth_buffer),
            ctypes.byref(out_auth_buffer_size),
            ctypes.byref(f_save),
            1
        )

        return resultado == 0
    except Exception:
        return False