from pydantic import BaseModel, field_validator
from datetime import datetime


class ProcessData(BaseModel):
    date_base: str

    @field_validator('date_base')
    @classmethod
    def validate_fecha(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("The date is not in the correct format (YYYY-MM-DD)")
        return v


class ProcessDataResponse(BaseModel):
    message: str
