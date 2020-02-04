from .techniques import router as techniques_router
from .temtems import router as temtem_router
from .traits import router as traits_router
from .items import router as items_router

routers = [
    ('/temtems', temtem_router),
    ('/traits', traits_router),
    ('/items', items_router),
    ('/techniques', techniques_router),
]
