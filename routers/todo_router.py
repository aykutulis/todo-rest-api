from fastapi import APIRouter
from models.TodoModel import TodoModel
from schemas import CreateTodoSchema, UpdateTodoSchema
from exceptions.TodoNotFoundException import TodoNotFoundException
from exceptions.AuthenticationException import AuthenticationException
from utils.database_utils import db_dependency
from utils.auth_utils import current_user_dependency

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@router.get("")
def get_user_todos(user: current_user_dependency, db: db_dependency):

    if user is None:
        raise AuthenticationException()

    return db.query(TodoModel).filter(TodoModel.owner_id == user['id']).all()


@router.get("/{id}")
def get_todo(id: int, user: current_user_dependency, db: db_dependency):

    if user is None:
        raise AuthenticationException()

    todo = db.query(TodoModel).filter(
        TodoModel.id == id,
        TodoModel.owner_id == user['id']
    ).first()

    if not todo:
        raise TodoNotFoundException()

    return todo


@router.post("")
def create_todo(user: current_user_dependency, todo: CreateTodoSchema, db: db_dependency):
    if not user:
        raise AuthenticationException()

    new_todo = TodoModel(**todo.dict(), owner_id=user['id'])
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put("/{id}")
def update_todo(id: int, todo: UpdateTodoSchema, db: db_dependency):
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
def delete_todo(id: int, db: db_dependency):
    todo = db.query(TodoModel).filter(TodoModel.id == id).first()

    if not todo:
        raise TodoNotFoundException()

    db.delete(todo)
    db.commit()

    return {"message": "Todo deleted successfully"}
