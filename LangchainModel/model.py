import os
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = init_chat_model("llama3-8b-8192", model_provider="groq")

def review_cv(cv_data):
    prompt = f"""
    Review the following CV and rate it on a scale of 1 to 10. Also, recommend the most suitable profession.

    Name: {cv_data['name']}
    Education: {cv_data['education']}
    Experience: {cv_data['experience']}
    Skills: {cv_data['skill']}
    Summary: {cv_data['summary']}

    Provide your response in JSON format:
    {{"rating": <score>, "profession_recommendation": "<profession>"}}
    """

    response = model.invoke([HumanMessage(content=prompt)])
    return response.content