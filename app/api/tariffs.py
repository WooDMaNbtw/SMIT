import json
from datetime import datetime, timedelta
from core.config import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile
from core.models import Tariff

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_tariffs(file: UploadFile, db: Session = Depends(get_db)):
    try:
        content = await file.read()
        tariffs_data = json.loads(content)

        for date_str, tariffs in tariffs_data.items():
            start_date = datetime.strptime(date_str, "%Y-%m-%d")
            for tariff in tariffs:
                new_tariff = Tariff(
                    cargo_type=tariff["cargo_type"],
                    rate=tariff["rate"],
                    start_date=start_date,
                    end_date=start_date + timedelta(days=30)
                )
                print(tariff)
                db.add(new_tariff)

        db.commit()
        return {"status": "success", "message": "Tariffs uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")


# @router.post("/tariffs", status_code=status.HTTP_201_CREATED)
# async def create_tariff(payload: TariffBaseSchema, db: Session = Depends(get_db)):
#     new_tariff = Tariff(**payload.dict())
#
#     db.add(new_tariff)
#     db.commit()
#     db.refresh()
#
#     return {
#         "status": "success",
#         "tariff": new_tariff
#     }
#
# @router.get("/tariffs")
# async def get_tariff(db: Session = Depends(get_db)):
#     tariffs = db.query(Tariff).all()
#     return {
#         "status": "success",
#         "results": len(tariffs),
#         "tariffs": tariffs
#     }
#
# @router.get("/tariffs/{tariffId}")
# async def retrieve_tariff(tariffId: str, db: Session = Depends(get_db)):
#     tariff = db.query(Tariff).filter(Tariff.id == tariffId).first()
#     if not tariff:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No tariff was found with id: {tariffId}"
#         )
#     return {
#         "status": "success",
#         "tariff": tariff
#     }

@router.delete('/{tariffId}')
def delete_tariff(tariffId: str, db: Session = Depends(get_db)):
    tariff_query = db.query(Tariff).filter(Tariff.id == tariffId)
    tariff = tariff_query.first()
    if not tariff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No tariff was found with id: {tariffId}')
    tariff_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
