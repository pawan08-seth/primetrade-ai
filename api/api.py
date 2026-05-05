from fastapi import APIRouter,Depends,HTTPException, status
from Models.Task_schemas import Create,Show,Update,ShowTask
from Auth.Dependencies import get_current_user,require_role
from Database.database import Base,engine,get_db
from sqlalchemy.orm import Session
from Models.table import Task,Users
from sqlalchemy import func,desc
from typing import Optional
from datetime import date
from Models.Status import Latest

router=APIRouter(prefix="/CRUD/v1",tags=["CRUD"])
Base.metadata.create_all(bind=engine)

@router.post("/Create",response_model=Show)
def Create(request:Create,db:Session = Depends(get_db),current_user=Depends((require_role(["Admin"])))):
    Create_task=Task(amount=request.amount,
                     category=request.category,
                     Date=request.Date,
                     notes=request.notes,
                     owner_id=current_user.id)
    db.add(Create_task)
    db.commit()
    db.refresh(Create_task)
    return Create_task

@router.get("/task/{id}",response_model=Show)
def Get_Task(id:int,db:Session=Depends(get_db),current_user=Depends((require_role(["Admin","Analyst"])))):
    task=db.query(Task).filter(Task.id==id,Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with the id {id} is not available")
    
    return task

@router.get("/filter")
def get_tasks(
    id: Optional[int] = None,
    category: Optional[str] = None,
    Date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Admin", "Analyst"]))):
    if not any([id, category, Date]):
        raise HTTPException(
            status_code=400,
            detail="At least one filter is required")

    query = db.query(Task).filter(
        Task.owner_id == current_user.id
    )

    if id:
        task = query.filter(Task.id == id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    if category:
        query = query.filter(
            func.lower(Task.category) == category.lower()
        )

    if Date:
        query = query.filter(Task.Date == Date)

    return query.all()
    


@router.get("/tasks")
def Tasks(db:Session=Depends(get_db),current_user=Depends((require_role(["Admin","Analyst"])))):
        try:  
            tasks=db.query(Task).filter(Task.owner_id==current_user.id).all()
            return tasks
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Task available")

@router.patch("/tasks/{task_id}", response_model=Show)
def update_task(
    task_id: int,
    updated_data: Update,
    db: Session = Depends(get_db),
    current_user=Depends((require_role(["Admin"])))):
    
    task = db.query(Task).filter(Task.id == task_id,Task.owner_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    
    if updated_data.amount is not None:
        task.amount = updated_data.amount

    if updated_data.category is not None:
        task.category = updated_data.category

    if updated_data.notes is not None:
        task.notes= updated_data.notes

    db.commit()
    db.refresh(task)

    return task

@router.delete("/{id}")
def delete_todo(id: int,db: Session = Depends(get_db),current_user=Depends((require_role(["Admin"])))):
    db_todo = db.query(Task).filter(id==Task.id,Task.owner_id == current_user.id).first()

    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Only owner or admin can delete
    if current_user.roles != "admin" and db_todo.owner_id != current_user.id:
      raise HTTPException(status_code=403, detail="Not authorized to delete this todo")

    db.delete(db_todo)
    db.commit()

    return {"message": "Deleted successfully"},status.HTTP_200_OK

@router.get("/summary")
def Dashboard(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    try: 
        tasks=db.query(Task).filter(Task.owner_id==current_user.id).all()
        if tasks:
            Status=Latest(db)
            total = db.query(func.sum(Task.amount)).scalar() or 0
            Total_income=db.query(func.sum(Task.amount)).filter(Task.category=="income").scalar() or 0
            Total_expense=db.query(func.sum(Task.amount)).filter(Task.category=="expense").scalar() or 0
            net_balance=Total_income-Total_expense
            return {"message": "Dashboard data fetched successfully",
                    "data": {"Total":[{"total_amount": total}],
                             "Categorywise Total":[{"total_income": Total_income,
                    "total_expense": Total_expense}],
                    "net_balance": net_balance,
                    "current_status": Status}}
        else:
            return {
                "Total": 0,
                "Income": 0,
                "Expense": 0,
                "Net_balance": 0,
                "Current_Status": None}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Dashboard error: {str(e)}"
        )
    


        

