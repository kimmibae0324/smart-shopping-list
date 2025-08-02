# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .recommender import recommend_recipes

app = FastAPI()

class IngredientsRequest(BaseModel):
    ingredients: List[str]

@app.post("/recommend")
def get_recommendations(request: IngredientsRequest):
    return {"recommendations": recommend_recipes(request.ingredients)}
