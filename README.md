# CV Insighter : A FastAPI CV Reviewer  

This project is a FastAPI-based application that reviews CVs using Groq AI's API. It evaluates CV data, provides a rating (1-10), and suggests a suitable profession based on the information provided. The application uses PostgreSQL as the database and SQLAlchemy for ORM, with Llama 3-8B as the chat model.

## Features

- Accepts CV data including name, education, experience, skills, and summary.
- Sends CV data to Groq AI's Llama 3-8B model for review and rating.
- Provides a profession recommendation based on AI analysis.
- Uses PostgreSQL as the database backend.
- Implements SQLAlchemy for ORM.

## Technologies Used

- **FastAPI** - Web framework for building APIs.
- **Groq AI API** - AI-powered analysis using Llama 3-8B. #Previous version
- **Llama3.2-8b** - Locally ran model through Ollama. #Newer Version
- **PostgreSQL** - Database for storing CV data.
- **SQLAlchemy** - ORM for database interaction.
- **Pydantic** - Data validation and serialization.

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL database
- Ollama Llama3.2 model

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/RafinEazdan/CV-Insighter.git
   cd CV_Insighter
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```sh
   export DATABASE_URL="postgresql://user:password@localhost:5432/cv_db"
   ```

5. Apply database migrations:
   ```sh
   alembic upgrade head
   ```

6. Run the FastAPI server:
   ```sh
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Submit CV for Review
```http
POST /review-cv/
```
**Request Body:**
```json
{
  "name": "John Doe",
  "education": "MSc Computer Science",
  "experience": "5 years in Software Development",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "summary": "Experienced backend developer specializing in APIs."
}
```
**Response:**
```json
{
  "rating": 8,
  "rating_analysis": "The CV is well-structured and effectively communicates Michael's skills and experience. However, it would be beneficial to include specific achievements and metrics to demonstrate the impact of his work. Additionally, a brief description of his role and responsibilities at each company would add more context.",
  "profession_recommendation": "Software Developer"
}
```
### Compare Between two or more CVs 
```http
POST /compare-cv/
```

**Request Body:**
```json
{
  "cv_list": [
    Id_of_CV_1,
    ID_of_CV_2
  ]
}
```
**Response:**
```json
{
  "industry_recommendations": [
    {
      "cv_index": 0,
      "industry": "Museums and Archives"
    },
    {
      "cv_index": 1,
      "industry": "Research and Development in Physics"
    }
  ],
  "summary_analysis": "The first CV is well-suited for the museums and archives industry due to the candidate's background in history and experience as an archivist. The second CV is suitable for the research and development industry in physics, given the candidate's education and experience in the field."
}
```

## Contributions
Feel free to fork the repo, open issues, and submit pull requests!

## Author
Eazdan Mostafa Rafin (https://github.com/RafinEazdan)
