from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/expenses/", response_model=schemas.ExpenseOut)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    created_expense = crud.add_expense(db, expense, created_by=1)  # Check what this returns

    # If created_expense is a dictionary, access keys directly instead of attributes
    return {
        "id": created_expense.get("id"),  # Use get method for safe access
        "amount": created_expense.get("amount"),
        "description": created_expense.get("description"),
        "created_by": 1,  # Adjust as necessary
        "splits": [
            {"user_id": participant, "amount_owed": created_expense["amount"] / len(expense.participants), "split_method": expense.split_method, "amount": created_expense["amount"] / len(expense.participants)}
            for participant in expense.participants
        ]
    }

@app.get("/expenses/user/{user_id}")
def get_user_expenses(user_id: int, db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).filter(models.Expense.created_by == user_id).all()
    return expenses


@app.get("/expenses/balance-sheet/")
def download_balance_sheet(db: Session = Depends(get_db)):
    balance_sheet = crud.generate_balance_sheet(db)
    return balance_sheet 