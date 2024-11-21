from fastapi import FastAPI, Request
from api.insurance import router as insurance_router
from api.tariffs import router as tariffs_router
from fastapi.responses import HTMLResponse
from core.config import BaseModel, engine
from fastapi.templating import Jinja2Templates

BaseModel.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.include_router(insurance_router, prefix="/api/v0/insurance", tags=["Insurance"])
app.include_router(tariffs_router, prefix="/api/v0/tariffs", tags=["Tariffs"])

@app.get("/api/healthchecker")
def root():
    return {"message": "Hello, world!"}

@app.get("/", response_class=HTMLResponse)
async def upload_tariffs_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})