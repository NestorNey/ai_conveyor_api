import os
import gc
import logging
import asyncio

from src import database
from settings import device_mapping
from src.websocket.FlowStateWSManager import manager as flow_state_ws_manager

from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory 

from time import sleep

from josneslib import Flow, FlowRunner

logger = logging.getLogger(__name__)

os.environ['GPIOZERO_PIN_FACTORY'] = 'lgpio'
Device.pin_factory = LGPIOFactory()

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
        Inicia el flow en background de forma segura.
        """
        try:
            logger.info(f"[StartFlowUseCase] Iniciando flow '{self.flow_name}'")
            
            # 1. Detener flow anterior si existe
            if database.flow_running is not None:
                logger.warning("⚠️ Deteniendo flow anterior...")
                database.flow_running.stop()
                database.flow_running = None
                sleep(0.5) # Tiempo suficiente para liberar /dev/video0
                        
            # 2. Limpieza de hardware
            _reset_gpio_pins()
            
            # 3. Convertir diccionarios a instancias de dispositivos
            converted_config = Flow.convert_options_to_instances(self.flow_options, device_mapping)
            
            # 4. Obtener la clase del Flow
            FlowClass = database.in_memory_db.get_flow(self.flow_name)
            if not FlowClass:
                raise ValueError(f"Flow '{self.flow_name}' no encontrado")
            
            # 5. Crear instancia del flow
            flow_instance = FlowClass(converted_config)
            
            # --- EL ARREGLO DEL LOOP ---
            # En lugar de buscar el loop en el hilo actual (que falla), 
            # se lo pedimos al manager del WebSocket o lo buscamos globalmente.
            
            def socket_state_callback(payload):
                # Intentamos obtener el loop donde vive el WebSocket
                loop = None
                try:
                    # Si el manager ya guardó el loop al conectar, úsalo
                    if hasattr(flow_state_ws_manager, 'loop') and flow_state_ws_manager.loop:
                        loop = flow_state_ws_manager.loop
                    else:
                        # Si no, intenta pescar el loop principal
                        loop = asyncio.get_running_loop()
                except RuntimeError:
                    pass

                if loop and loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        flow_state_ws_manager.broadcast(payload), 
                        loop
                    )
                else:
                    # Fallback por si el WS no está listo aún
                    logger.debug(f"Socket no listo. Payload: {payload['state']}")

            # Asignamos el callback seguro
            flow_instance.set_state_callback(socket_state_callback)
            
            # 6. Crear runner e iniciar
            runner = FlowRunner(flow_instance)
            runner.start()
            
            # 7. Guardar globalmente
            database.flow_running = runner
            logger.info(f"[StartFlowUseCase] ✅ Flow '{self.flow_name}' ON")
            
            return {
                "success": True,
                "message": f"Flow '{self.flow_name}' iniciado",
                "flow_name": self.flow_name
            }
            
        except Exception as e:
            logger.error(f"[StartFlowUseCase] ❌ Error crítico: {str(e)}", exc_info=True)
            # Limpieza en caso de error para no dejar la cámara trabada
            if database.flow_running:
                database.flow_running.stop()
                database.flow_running = None
            raise