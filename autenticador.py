import ctypes
from ctypes import wintypes

def verificar_biometria_ltsc():
    """Invoca el cuadro de diálogo nativo de credenciales de Windows, 
    autocompletando el usuario actual para una validación rápida."""
    class CREDUI_INFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("hwndParent", wintypes.HWND),
            ("pszMessageText", wintypes.LPCWSTR),
            ("pszCaptionText", wintypes.LPCWSTR),
            ("hbmBanner", wintypes.HBITMAP),
        ]

    # Cargamos la librería nativa de credenciales del sistema
    credui = ctypes.windll.credui

    info = CREDUI_INFO()
    info.cbSize = ctypes.sizeof(CREDUI_INFO)
    info.hwndParent = None
    info.pszMessageText = "Confirme su identidad para acceder a Finanzas."
    info.pszCaptionText = "Seguridad del Sistema - Finanzas"
    info.hbmBanner = None

    auth_package = wintypes.ULONG(0)
    out_auth_buffer = ctypes.c_void_p()
    out_auth_buffer_size = wintypes.ULONG(0)
    save = wintypes.BOOL(False)

    # 0x00000002 corresponde a CREDUI_FLAGS_COMPLETE_USERNAME 
    # para tomar el usuario actual de la computadora en automático.
    resultado = credui.CredUIPromptForWindowsCredentialsW(
        ctypes.byref(info),
        0,
        ctypes.byref(auth_package),
        None,
        0,
        ctypes.byref(out_auth_buffer),
        ctypes.byref(out_auth_buffer_size),
        ctypes.byref(save),
        0x00000002  
    )

    # Si el usuario se autentica correctamente (ERROR_SUCCESS)
    if resultado == 0:
        if out_auth_buffer:
            ctypes.windll.ole32.CoTaskMemFree(out_auth_buffer)
        return True
    
    return False

if __name__ == "__main__":
    print("Iniciando autenticación nativa...")
    if verificar_biometria_ltsc():
        print("¡Acceso concedido! Entrando al sistema de finanzas...")
    else:
        print("Acceso cancelado o denegado.")