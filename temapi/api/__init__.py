from fastapi import FastAPI
from .routes import routers

app = FastAPI()

for (prefix, router) in routers:
    app.include_router(router, prefix=prefix)
