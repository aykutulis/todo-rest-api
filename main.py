from fastapi import FastAPI
from utils.database_utils import Base, engine
from routers import todo_router, auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router)
app.include_router(auth_router)
