from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Farm AI Industrial System",
    version="1.0.0"
)

# -----------------------------
# Request Schema
# -----------------------------
class FeedRequest(BaseModel):
    animal: str
    age: int
    goal: str
    available: Optional[List[str]] = []

# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Farm AI API is running"
    }

# -----------------------------
# AI Optimization Endpoint
# -----------------------------
@app.post("/ai/optimize-ration")
def optimize_ration(req: FeedRequest):

    # -----------------------------
    # Simple AI logic (demo version)
    # -----------------------------
    base = {
        "corn": 40,
        "soybean_meal": 30,
        "wheat_bran": 15,
        "barley": 10,
        "minerals_vitamins": 3,
        "oil": 2
    }

    # Adjust based on age
    if req.age < 10:
        base["soybean_meal"] += 5
        base["corn"] -= 5

    # Goal adjustment
    if req.goal == "growth":
        base["soybean_meal"] += 3
        base["corn"] += 2

    if req.goal == "cost":
        base["corn"] += 5
        base["soybean_meal"] -= 5

    # Available ingredients filter
    if req.available:
        base = {k: v for k, v in base.items() if k in req.available}

    return {
        "animal": req.animal,
        "age": req.age,
        "goal": req.goal,
        "ration": base,
        "note": "AI optimized ration (industrial v1)"
    }