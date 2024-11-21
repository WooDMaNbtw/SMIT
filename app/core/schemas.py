from datetime import datetime


class TariffBaseSchema:
    id: str | None = None
    cargoType: str
    rate: str
    startDate: datetime
    endDate: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
