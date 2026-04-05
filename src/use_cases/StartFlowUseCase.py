from src import database

from gpiozero import Servo, Device
import logging
import gc

from time import sleep

from josneslib import Flow, FlowRunner
from josneslib.devices import MotorL298N, Picamera2Wrapper

logger = logging.getLogger(__name__)

def _reset_gpio_pins():
    """
    Limpieza segura de recursos.
    """
    try:
        logger.debug("[_reset_gpio_pins] Ejecutando Garbage Collector...")
        # Esto destruye los objetos que ya no tienen referencia (los del flow anterior)
        # Al destruirse, el método __del__ de gpiozero libera los pines.
        gc.collect() 
    except Exception as e:
        logger.error(f"[_reset_gpio_pins] Error: {e}")

class StartFlowUseCase:
    def __init__(self, flow_name: str, flow_options: dict):
        self.flow_name = flow_name
        self.flow_options = flow_options

    def execute(self) -> dict:
        """
        Inicia el flow en background.
        """
        
        try:
            logger.info(f"[StartFlowUseCase] Iniciando flow '{self.flow_name}'")
            
            # Detener flow anterior si existe
            if database.flow_running is not None:
                database.flow_running.stop()
                database.flow_running = None
                import gc
                gc.collect()
                sleep(0.5) # <--- Dale medio segundo real al hardware para resetearse
                        
            # Resetear pines GPIO para evitar conflictos
            logger.debug("[StartFlowUseCase] Reseteando pines GPIO")
            _reset_gpio_pins()
            
            # Mapeo de tipos a clases
            device_map = {
                "Servo": Servo,
                "MotorL298N": MotorL298N,
                "Picamera2": Picamera2Wrapper  # ← Usa el wrapper con constructor compatible
            }
            logger.debug(f"[StartFlowUseCase] Device map configurado: {list(device_map.keys())}")
            
            # Convertir diccionarios a instancias de dispositivos
            logger.debug(f"[StartFlowUseCase] Convirtiendo opciones... {self.flow_options.keys()}")
            converted_config = Flow.convert_options_to_instances(self.flow_options, device_map)
            logger.debug(f"[StartFlowUseCase] Opciones convertidas: {converted_config.keys()}")
            
            # Obtener la clase del Flow
            logger.debug(f"[StartFlowUseCase] Buscando flow '{self.flow_name}' en la BD")
            FlowClass = database.in_memory_db.get_flow(self.flow_name)
            if not FlowClass:
                raise ValueError(f"Flow '{self.flow_name}' no encontrado en la base de datos")
            logger.debug(f"[StartFlowUseCase] Flow encontrado: {FlowClass}")
            
            # Crear instancia del flow
            logger.debug("[StartFlowUseCase] Creando instancia del Flow")
            flow_instance = FlowClass(converted_config)
            logger.debug(f"[StartFlowUseCase] Flow instanciado: {flow_instance}")
            
            # Crear runner
            logger.debug("[StartFlowUseCase] Creando FlowRunner")
            runner = FlowRunner(flow_instance)
            
            # Iniciar
            logger.debug("[StartFlowUseCase] Iniciando runner en background")
            runner.start()
            
            # Guardar globalmente
            database.flow_running = runner
            logger.info(f"[StartFlowUseCase] ✅ Flow '{self.flow_name}' iniciado exitosamente")
            
            return {
                "success": True,
                "message": f"Flow '{self.flow_name}' iniciado exitosamente",
                "flow_name": self.flow_name
            }
            
        except Exception as e:
            logger.error(f"[StartFlowUseCase] ❌ Error al iniciar flow: {str(e)}", exc_info=True)
            raise