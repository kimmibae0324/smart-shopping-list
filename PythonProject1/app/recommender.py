# app/recommender.py
import pandas as pd
import os
from sentence_transformers import SentenceTransformer, util
from .utils import normalize

base_dir = os.path.dirname(__file__)
recipes = pd.read_csv(os.path.join(base_dir, "recipes.csv"))
kurly = pd.read_csv(os.path.join(base_dir, "kurly.csv"))

model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

def recommend_recipes(user_ingredients):
    user_ingredients = [normalize(i) for i in user_ingredients]
    user_embeds = model.encode(user_ingredients, convert_to_tensor=True)

    results = []

    for _, row in recipes.iterrows():
        recipe_ings = [normalize(i) for i in row["재료"].split(",")]
        have, need = [], []
        total_cost = 0

        for ing in recipe_ings:
            ing_embed = model.encode(ing, convert_to_tensor=True)
            cosine_scores = util.cos_sim(ing_embed, user_embeds)
            if cosine_scores.max().item() > 0.7:
                have.append(ing)
            else:
                need.append(ing)

        if not have:
            continue

        match_score = len(have) / len(recipe_ings)

        items = []
        for ing in need:
            match = kurly[kurly['정규이름'].str.contains(ing, na=False)]
            for _, r in match.head(2).iterrows():
                items.append({
                    "재료명": ing,
                    "이름": r["이름"],
                    "가격": r["가격"],
                    "단위": r["단위"]
                })
                total_cost += r["가격"]

        results.append({
            "메뉴": row['메뉴'],
            "매칭률": round(match_score, 2),
            "부족재료": need,
            "레시피": row['레시피'],
            "추천상품": items
        })

    return sorted(results, key=lambda x: x['매칭률'], reverse=True)[:5]
