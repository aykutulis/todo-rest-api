from fastapi import APIRouter, Depends
from models.TodoModel import TodoModel
from schemas import CreateTodoSchema, UpdateTodoSchema
from sqlalchemy.orm import Session
from exceptions.TodoNotFoundException import TodoNotFoundException
from utils.database import get_db

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@router.get("")
def get_all_todos(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()


@router.get("/{id}")
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not todo:
        raise TodoNotFoundException()

    return todo


@router.post("")
def create_todo(todo: CreateTodoSchema, db: Session = Depends(get_db)):
    new_todo = TodoModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put("/{id}")
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


@router.delete("/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not todo:
        raise TodoNotFoundException()

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
