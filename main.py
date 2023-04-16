from fastapi import FastAPI
from database import Base
from database import engine
from routers import todo_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router)
