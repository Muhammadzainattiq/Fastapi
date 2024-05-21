#Here i am making the fastapi CRUD endpoints for my todo app


from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, Todo, engine  # Import from database.py

app = FastAPI()


# Dependency function to inject database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for Todo data
class TodoIn(BaseModel):
    title: str
    description: str


class TodoOut(BaseModel):
    id: int
    title: str
    description: str


@app.post('/todos/')
async def create_todo(todo: TodoIn, db: Session = Depends(get_db)):
    new_todo = Todo(title=todo.title, description=todo.description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)  # Optional, might be unnecessary (check SQLAlchemy docs)
    return TodoOut(**new_todo.dict())  # Return TodoOut model with data


@app.put('/todos/{todo_id}')
async def update_todo(updated_todo: TodoIn, todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.title = updated_todo.title
    db_todo.description = updated_todo.description
    db.commit()
    return TodoOut(**db_todo.dict())  # Return TodoOut model with updated data


@app.delete('/todos/{todo_id}')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}

# Run the application using uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Adjust host/port if needed
