from fastapi import FastAPI, Depends, HTTPException
from models.TodoModel import TodoModel
from database import Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from database import Base
from exceptions.TodoNotFoundException import TodoNotFoundException

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/todos")
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


@app.get("/todos/{id}")
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not todo:
        raise TodoNotFoundException()

    return todo
