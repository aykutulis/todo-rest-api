from fastapi import FastAPI, Depends
from models.TodoModel import TodoModel
from schemas import CreateTodoSchema, UpdateTodoSchema
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


@app.post("/todos")
def create_todo(todo: CreateTodoSchema, db: Session = Depends(get_db)):
    new_todo = TodoModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put("/todos/{id}")
def update_todo(id: int, todo: UpdateTodoSchema, db: Session = Depends(get_db)):
    existing_todo = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not existing_todo:
        raise TodoNotFoundException()

    for key, value in todo.dict().items():
        if value is not None:
            setattr(existing_todo, key, value)

    db.commit()

    db.refresh(existing_todo)

    return existing_todo
