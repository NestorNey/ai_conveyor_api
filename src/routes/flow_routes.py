from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status

from src.schemas import FlowList, FlowSchema, FlowStartRequest
from src import database
from src.use_cases import StartFlowUseCase

from fastapi.responses import StreamingResponse, HTMLResponse

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
    database.in_memory_db.load_flows()
    return {"message": "Flows recargados correctamente"}

@router.get("/is_running/")
def is_flow_running():
    """Verificar si hay un Flow en ejecución"""
    return {"is_running": database.flow_running is not None}

@router.post("/start/")
def start_flow(flow_start_request: FlowStartRequest):
    """Iniciar un Flow por nombre con su configuración"""
    try:
        use_case = StartFlowUseCase(flow_name=flow_start_request.name, flow_options=flow_start_request.options)
        result = use_case.execute()
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
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
