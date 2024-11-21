from sqlalchemy import Column, Integer, String, Float, DateTime
from core.config import BaseModel, engine

class Tariff(BaseModel):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, index=True)
    cargo_type = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    def to_representation(self):
        return {
            "id": self.id,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "start_date": self.start_date,
            "end_date": self.end_date
        }

BaseModel.metadata.create_all(engine)