import uvicorn
from fastapi import FastAPI

from routers import router_tasks, router_ws
from core.config import settings
from database import Base, engine
from database.models import init_models

init_models()
Base.metadata.create_all(bind=engine)

app = FastAPI()

# adding routers to app
app.include_router(router_tasks.router, prefix='/tasks', tags=['tasks'])
app.include_router(router_ws.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=True)
