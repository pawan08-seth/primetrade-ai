from pydantic import BaseModel,Field,model_validator,ValidationError
from typing import Optional, Literal
from datetime import date

class Create(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount")
    category: Literal["income", "expense"] = Field(..., description="Type of transaction")
    Date: date = Field(..., description="Transaction date")
    notes: Optional[str] = Field(None, max_length=255, description="Optional description")

class Update(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[Literal["income", "expense"]] = None
    notes: Optional[str] = Field(None, max_length=255)

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        if not any(self.model_dump(exclude_none=True).values()):
            raise ValueError("At least one field is required")
        return self

class ShowTask(Create):
    id:int
    
class Show(BaseModel):
    id:int
    amount:float
    category:str
    Date:date
    notes:str

    model_config = {
        "from_attributes": True
    }
    




