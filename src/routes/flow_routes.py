from typing import List

from sqlalchemy.orm import Session

from src import database
from src.schemas import FlowList, FlowSchema, FlowStartRequest, FlowPresetSchema
from src.use_cases import StartFlowUseCase
from src.websocket.FlowStateWSManager import manager as flow_state_ws_manager
from src.repositories import FlowPresetRepository

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Body, Depends, HTTPException, status, WebSocket

router = APIRouter(prefix="/flows", tags=["flows"])

@router.get("/name/{name}", response_model=FlowSchema)
def get_flow_by_name(name: str):
    """Obtener un Flow por nombre"""
    flow = database.in_memory_db.get_flow_options_schema(name)
    
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow con nombre '{name}' no encontrado"
        )
        
    return flow

@router.get("/", response_model=FlowList)
def list_flows():
    """Listar todos los Flows disponibles"""
    flows_list = database.in_memory_db.list_flows()
    return {"flows_list": flows_list}

@router.get("/reload/")
def reload_flows():
    """Recargar los Flows disponibles"""
    database.in_memory_db.reload_flows()
    return {"message": "Flows recargados correctamente"}

@router.get("/is_running/")
def is_flow_running():
    """Verificar si hay un Flow en ejecución"""
    return {"is_running": database.flow_running is not None}

@router.post("/start/")
async def start_flow(flow_start_request: FlowStartRequest):
    """
    Iniciar un Flow por nombre con su configuración.
    Se usa 'async def' para asegurar que el UseCase pueda capturar 
    el loop de eventos principal de FastAPI.
    """
    try:
        # Al ser una ruta async, asyncio.get_running_loop() funcionará 
        # dentro del UseCase si se llama desde aquí.
        use_case = StartFlowUseCase(
            flow_name=flow_start_request.name, 
            flow_options=flow_start_request.options
        )
        
        # Ejecutamos el inicio del flow
        result = use_case.execute()
        return result

    except ValueError as e:
        print(f"Flow no encontrado: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"Error crítico en /start/: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar el Flow: {str(e)}"
        )
        
@router.get("/stream")
def stream():
    if database.flow_running is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay ningún Flow en ejecución"
        )
        
    flow = database.flow_running.get_flow()
    if not hasattr(flow, "stream"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El Flow en ejecución no tiene capacidad de streaming"
        )
    
    return StreamingResponse(
        database.flow_running.get_flow().stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.get("/stop", response_model=dict)
def stop_flow():
    if database.flow_running is None:
        raise HTTPException(status_code=404, detail="No hay Flow")
    
    database.flow_running.stop()
    # ESTO ES LO QUE TE FALTA:
    database.flow_running = None  # Liberar la referencia para que Python limpie
    return {"message": "Flow detenido correctamente"}

@router.websocket("/status")
async def websocket_status(websocket: WebSocket):
    await flow_state_ws_manager.connect(websocket)
    
    # Mandamos un estado inicial apenas se conecte para que no vea la pantalla vacía
    if database.flow_running is not None:
        flow = database.flow_running.flow  # Acceso directo a la instancia
        initial_data = {
            "flow_name": flow.name,
            "state": getattr(flow, "state", "unknown"),
            "data": {"message": "Conectado correctamente"}
        }
        await websocket.send_json(initial_data)
    else:
        await websocket.send_json({"flow_name": None, "state": "stopped"})

    try:
        # El bucle ahora solo sirve para mantener la conexión viva
        # y esperar a que el cliente se desconecte.
        while True:
            # Esperamos cualquier mensaje del cliente (o simplemente que siga ahí)
            data = await websocket.receive_text()
            
    except Exception as e:
        print(f"📡 WebSocket desconectado o error: {e}")
    finally:
        flow_state_ws_manager.disconnect(websocket)
        
@router.post("/presets", response_model=FlowPresetSchema)
def save_preset(preset: FlowPresetSchema, db: Session = Depends(database.get_db)):
    return FlowPresetRepository.create(db, preset)

@router.get("/presets/{flow_name}", response_model=List[FlowPresetSchema])
def list_presets(flow_name: str, db: Session = Depends(database.get_db)):
    return FlowPresetRepository.get_by_flow(db, flow_name)

@router.delete("/presets/{preset_id}")
def delete_preset(preset_id: int, db: Session = Depends(database.get_db)):
    success = FlowPresetRepository.delete(db, preset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Preset no encontrado")
    return {"message": "Preset eliminado correctamente"}

@router.put("/presets/{preset_id}", response_model=FlowPresetSchema)
def update_preset_options(
    preset_id: int, 
    new_options: dict = Body(...), # Esto obliga a leer el JSON entero como el dict
    db: Session = Depends(database.get_db)
):
    updated_preset = FlowPresetRepository.update_options(db, preset_id, new_options)
    if not updated_preset:
        raise HTTPException(status_code=404, detail="Preset no encontrado")
    return updated_preset