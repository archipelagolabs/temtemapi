from .temtems import router as temtem_router
from .traits import router as traits_router

routers = [
    ('/temtems', temtem_router),
    ('/traits', traits_router),
]
