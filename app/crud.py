from sqlalchemy.orm import Session
from . import models, schemas

def add_expense(db: Session, expense: schemas.ExpenseCreate, created_by: int):
    # Validate participant IDs
    valid_users = db.query(models.User).filter(models.User.id.in_(expense.participants)).all()
    valid_user_ids = {user.id for user in valid_users}

    # Check for invalid participant IDs
    for participant in expense.participants:
        if participant not in valid_user_ids:
            raise ValueError(f"User ID {participant} does not exist.")

    # Proceed with adding the expense
    db_expense = models.Expense(amount=expense.amount, description=expense.description, created_by=created_by)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    # Split logic based on method
    if expense.split_method == 'equal':
        split_amount = expense.amount / len(expense.participants)
        for participant in expense.participants:
            db_split = models.ExpenseSplit(expense_id=db_expense.id, user_id=participant, split_method='equal', amount_owed=split_amount)
            db.add(db_split)

    elif expense.split_method == 'exact':
        # Handle exact split logic
        total_split = sum(participant.amount for participant in expense.participants)  # Adjust this as needed
        if total_split != expense.amount:
            raise ValueError("Total split amounts must equal the expense amount.")
        for participant in expense.participants:
            db_split = models.ExpenseSplit(expense_id=db_expense.id, user_id=participant.user_id, split_method='exact', amount_owed=participant.amount)
            db.add(db_split)

    elif expense.split_method == 'percentage':
        # Handle percentage split logic
        total_percentage = sum(participant.percentage for participant in expense.participants)
        if total_percentage != 100:
            raise ValueError("Percentages must add up to 100%.")
        for participant in expense.participants:
            split_amount = (participant.percentage / 100) * expense.amount
            db_split = models.ExpenseSplit(expense_id=db_expense.id, user_id=participant.user_id, split_method='percentage', amount_owed=split_amount)
            db.add(db_split)

    db.commit()

    # Serialize response data
    splits = [
        {"user_id": split.user_id, "amount_owed": split.amount_owed, "split_method": split.split_method}
        for split in db_expense.splits
    ]

    return {
        "id": db_expense.id,
        "amount": db_expense.amount,
        "description": db_expense.description,
        "splits": splits
    }

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, mobile=user.mobile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def generate_balance_sheet(db: Session):
    # Logic to calculate and return the balance sheet
    # This is a placeholder; implement your balance sheet logic here.
    expenses = db.query(models.Expense).all()
    total_expense = sum(expense.amount for expense in expenses)
    return {"total_expenses": total_expense}  # Modify this to match your balance sheet format


def get_user_expenses(db: Session, user_id: int):
    expenses = db.query(models.Expense).filter(models.Expense.created_by == user_id).all()
    return [schemas.ExpenseOut.from_orm(expense) for expense in expenses]