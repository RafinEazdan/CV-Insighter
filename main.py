from fastapi import FastAPI, Depends, HTTPException, status, Path
import Models.models
from Models.models import CVs
from Database.database import engine, SessionLocal
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field


app = FastAPI()

Models.models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class CVRequest(BaseModel):
    name: str = Field(min_length=2, max_length = 100)
    email: EmailStr
    phone: str = Field(min_length=7,max_length=15)   
    education: List[str] = Field(default=[])
    experience: List[str] = Field(default=[]) 
    skill: List[str] = Field(default=[])
    summary: str = Field(min_length = 0, max_length=1000)


@app.get("/", status_code = status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(CVs).all()


@app.get("/cv/{cv_id}",status_code = status.HTTP_200_OK)
async def read_cv(db: db_dependency, cv_id:int = Path(gt=0)):
    cv_model = db.query(CVs).filter(CVs.id == cv_id).first()
    if cv_model is not None:
        return cv_model
    raise HTTPException(status_code= 404, detail="CV not found.")



@app.post("/cv",status_code=status.HTTP_201_CREATED)
async def create_cv(db: db_dependency, cv_request: CVRequest):
    cv_model = CVs(**cv_request.dict())

    db.add(cv_model)
    db.commit()


@app.put("/cv/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_cv(db: db_dependency,cv_request:CVRequest,cv_id:int = Path(gt=0)):
    cv_model = db.query(CVs).filter(CVs.id == cv_id).first()
    if cv_model is None:
        raise HTTPException(status_code=404, detail="CV Not Found")
    
    cv_model.name = cv_request.name
    cv_model.email = cv_request.email
    cv_model.phone = cv_request.phone
    cv_model.education = cv_request.education
    cv_model.experience = cv_request.experience
    cv_model.skill = cv_request.skill
    cv_model.summary = cv_request.summary

    db.add(cv_model)
    db.commit()


@app.delete("/cv/{cv_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(db: db_dependency, cv_id:int = Path(gt=0)):
    cv_model = db.query(CVs).filter(CVs.id ==cv_id).first()
    if cv_model is None:
        raise HTTPException(status_code=404, detail='CV not found.')
    db.query(CVs).filter(CVs.id == cv_id).delete()
    db.commit()