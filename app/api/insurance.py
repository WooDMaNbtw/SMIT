from fastapi import Depends, HTTPException, status, APIRouter, Response
from core.models import Tariff
from datetime import datetime
from sqlalchemy.orm import Session
from core.config import get_db


router = APIRouter()

@router.post("/calculate")
async def calculate_insurance(
        cargo_type: str,
        declared_value: float,
        request_date: str,
        db: Session = Depends(get_db)
):
    date = datetime.strptime(request_date, "%Y-%m-%d")
    tariff = db.query(Tariff).filter(
        Tariff.cargo_type == cargo_type,
        Tariff.start_date <= date,
        Tariff.end_date >= date,
    ).first()

    if not tariff:
        raise HTTPException(
            status_code=404,
            detail="No tariff found for the given cargo type and date"
        )

    insurance_cost = declared_value * tariff.rate
    return {
        "cargo_type": cargo_type,
        "declared_value": declared_value,
        "rate": tariff.rate,
        "insurance_cost": insurance_cost
    }
