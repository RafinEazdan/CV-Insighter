from fastapi import FastAPI, Depends, HTTPException, status, Path
from LangchainModel.model import review_cv, compare_cvs
import Models.models
from Models.models import CVs
from Database.database import engine, SessionLocal
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Models.models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# compare cv class
class CVCompareRequest(BaseModel):
    cv_list: List[int] = Field(min_items=2)


class CVCompareResponse(BaseModel):
    industry_recommendations: List[dict]
    summary_analysis: str = Field(max_length=1000)


class CVRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=15)
    education: List[str]  # Use default_factory instead of default=[]
    experience: List[str]   # Use default_factory instead of default=[]
    skill: List[str]   # Use default_factory instead of default=[]
    summary: str = Field(min_length=0, max_length=1000)


# Langchain Model
class CVReviewResponse(BaseModel):
    rating: int
    rating_analysis: str
    profession_recommendation: str


# Get all the CVs
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(CVs).all()


# Get a specific CV
@app.get("/cv/{cv_id}", status_code=status.HTTP_200_OK)
async def read_cv(db: db_dependency, cv_id: int = Path(gt=0)):
    cv_model = db.query(CVs).filter(CVs.id == cv_id).first()
    if cv_model is not None:
        return cv_model
    raise HTTPException(status_code=404, detail="CV not found.")


# Create a new CV
@app.post("/cv", status_code=status.HTTP_201_CREATED)
async def create_cv(db: db_dependency, cv_request: CVRequest):
    cv_model = CVs(**cv_request.dict())

    db.add(cv_model)
    db.commit()
    return {"id": cv_model.id}


# Update a CV
@app.put("/cv/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_cv(db: db_dependency, cv_request: CVRequest, cv_id: int = Path(gt=0)):
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


# Delete a CV
@app.delete("/cv/{cv_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv(db: db_dependency, cv_id: int = Path(gt=0)):
    cv_model = db.query(CVs).filter(CVs.id == cv_id).first()
    if cv_model is None:
        raise HTTPException(status_code=404, detail='CV not found.')
    db.query(CVs).filter(CVs.id == cv_id).delete()
    db.commit()


# Review a CV
@app.get("/review_cv/{cv_id}", status_code=status.HTTP_200_OK, response_model=CVReviewResponse)
async def review_cv_endpoint(db: db_dependency, cv_id: int = Path(gt=0)):
    print("Database Session:", db)
    cv_model = db.query(CVs).filter(CVs.id == cv_id).first()

    if cv_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found")

    cv_data = {
        "name": cv_model.name,
        "education": cv_model.education,
        "experience": cv_model.experience,
        "skills": cv_model.skill,
        "summary": cv_model.summary,
    }

    try:
        review_response = review_cv(cv_data)
        return review_response
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Compare CVs
@app.post("/compare_cv", status_code=status.HTTP_200_OK, response_model=CVCompareResponse)
async def compare_cvs_endpoint(db: db_dependency, request: CVCompareRequest):
    cv_models = db.query(CVs).filter(CVs.id.in_(request.cv_list)).all()
    print(cv_models)
    if len(cv_models) < 2:
        raise HTTPException(status_code=400, detail="At least two valid CVs are required for comparison.")

    cv_list = []
    for cv in cv_models:
        cv_list.append({
            "name": cv.name,
            "education": cv.education,
            "experience": cv.experience,
            "skills": cv.skill,
            "summary": cv.summary,
        })

    try:
        comparison_response = compare_cvs(cv_list)
        return comparison_response
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))