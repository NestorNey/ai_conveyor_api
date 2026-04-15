from .camera_preset_routes import router as camera_preset_router
from .motor_reducer_routes import router as motor_reducer_router
from .servo_routes import router as servo_router
from .flow_routes import router as flow_router
from .devices_routes import ruter as devices_router
from .sys_routes import router as network_router

__all__ = [
    "camera_preset_router",
    "motor_reducer_router",
    "servo_router",
    "flow_router",
    "devices_router",
    "network_router"
]