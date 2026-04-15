import socket
import subprocess
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Creamos un router nuevo para todo lo que tenga que ver con la red
router = APIRouter(prefix="/network", tags=["network"])

# --- ESQUEMAS (Pydantic Models) ---
class WifiCredentials(BaseModel):
    ssid: str
    password: str

# --- RUTAS ---

@router.get("/ip")
def get_raspberry_ip():
    """
    Obtiene la IP local real de la Raspberry Pi en la red.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Hacemos una conexión falsa (no sale a internet) 
        # solo para obligar al SO a decidir qué interfaz de red usar y sacarle la IP.
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        # Si de plano no está conectada a nada, regresa localhost
        ip = '127.0.0.1'
    finally:
        s.close()
        
    return {"ip": ip}


@router.post("/wifi")
def connect_to_wifi(creds: WifiCredentials):
    """
    Conecta la Raspberry a una nueva red Wi-Fi.
    Requiere que el OS use NetworkManager (nmcli).
    """
    try:
        # Construimos el comando de consola. 
        # Ponemos comillas simples por si el SSID o Password tienen espacios.
        comando = f"sudo nmcli dev wifi connect '{creds.ssid}' password '{creds.password}'"
        
        # Ejecutamos el comando directo en el sistema operativo
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True
        )

        # returncode 0 significa que el comando se ejecutó sin errores
        if resultado.returncode == 0:
            return {"success": True, "message": f"Conectado exitosamente a {creds.ssid}"}
        else:
            # Si escribieron mal la contraseña o no existe la red, mandamos el error
            error_msg = resultado.stderr.strip() or resultado.stdout.strip()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Fallo la conexión: {error_msg}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error interno al intentar configurar el Wi-Fi: {str(e)}"
        )