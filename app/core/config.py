import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

environ.Env.read_env(BASE_DIR / '.env.local')

DATABASE_URL = os.getenv("DATABASE_URL", 'postgresql://admin:secret@localhost:5432/postgres')

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autoflush=False, bind=engine)

BaseModel = declarative_base()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()