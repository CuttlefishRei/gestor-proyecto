import ctypes
from ctypes import wintypes

def verificar_biometria_ltsc():
    """Esta función es como un 'guardia de seguridad' en la puerta que le pide 
    al sistema operativo de Windows que abra la ventanita de huella digital o PIN."""
    
    # Aquí creamos un 'formulario' o plantilla vacía que Windows nos pide llenar 
    # para saber cómo se va a ver el cuadro de diálogo (título, mensajes, etc.).
    class CREDUI_INFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("hwndParent", wintypes.HWND),
            ("pszMessageText", wintypes.LPCWSTR),
            ("pszCaptionText", wintypes.LPCWSTR),
            ("hbmBanner", wintypes.HBITMAP),
        ]

    # Llamamos a las herramientas secretas que Windows tiene guardadas en su caja de herramientas (librería nativa)
    credui = ctypes.windll.credui

    # Llenamos nuestro formulario con los letreros y mensajes que verá el usuario en su pantalla
    info = CREDUI_INFO()
    info.cbSize = ctypes.sizeof(CREDUI_INFO)
    info.hwndParent = None  # No depende de otra ventana, flota libremente
    info.pszMessageText = "Confirme su identidad para acceder a Finanzas."
    info.pszCaptionText = "Seguridad del Sistema - Finanzas"
    info.hbmBanner = None

    # Variables vacías donde Windows guardará la información de si pasaste la prueba o no
    auth_package = wintypes.ULONG(0)
    out_auth_buffer = ctypes.c_void_p()
    out_auth_buffer_size = wintypes.ULONG(0)
    save = wintypes.BOOL(False)

    # 0x00000002 es un código secreto para decirle a Windows: 
    # "Rellena el nombre del usuario que está usando la computadora ahorita en automático".
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

    # Si el resultado es 0 (que significa que todo salió bien y el usuario puso bien su huella/PIN)
    if resultado == 0:
        # Limpiamos la memoria RAM de la computadora por seguridad para que no queden datos sueltos
        if out_auth_buffer:
            ctypes.windll.ole32.CoTaskMemFree(out_auth_buffer)
        return True  # ¡Acceso autorizado! Devolvemos un "Sí" verdadero
    
    return False  # Si canceló o falló, devolvemos un "No"

# Esta pequeña sección sirve solo si corres este archivo solo para probarlo
if __name__ == "__main__":
    print("Iniciando autenticación nativa...")
    if verificar_biometria_ltsc():
        print("¡Acceso concedido! Entrando al sistema de finanzas...")
    else:
        print("Acceso cancelado o denegado.")