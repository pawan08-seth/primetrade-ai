from sqlalchemy.orm import Session
from Models.table import Task
from sqlalchemy import desc
from datetime import date

def Latest(db: Session):
    status=db.query(Task).order_by(desc(Task.Date)).first()
    if not status:
        return {"Status": "No Data"}

    days_diff = (date.today() - status.Date).days

    if days_diff > 30:
        return {"Status": "Inactive",
                "Last Activity": str(status.Date),
                "Days Since Last Activity": days_diff}
    else:
        return {"Status": "Active","Last Activity": str(status.Date)}