from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json

from database import SessionLocal, RationHistory, Base, engine

# ----------------------------
# DB INIT
# ----------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Farm AI Industrial System")

# ----------------------------
# DB Dependency
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# REQUEST MODEL
# ----------------------------
class FeedRequest(BaseModel):
    animal: str
    age: int
    goal: str
    available: list[str] = []

# ----------------------------
# AI OPTIMIZER (CORE ENGINE)
# ----------------------------
@app.post("/ai/optimize-ration")
def optimize_ration(req: FeedRequest, db: Session = Depends(get_db)):

    base = {
        "corn": 40,
        "soybean_meal": 25,
        "wheat_bran": 15,
        "barley": 10,
        "minerals_vitamins": 5,
        "oil": 3,
        "insect_protein": 2
    }

    notes = []
    recommendations = []

    # -----------------------
    # Animal logic
    # -----------------------
    if req.animal == "chicken":

        if req.age < 21:
            base["soybean_meal"] += 6
            base["corn"] += 4
            notes.append("Starter phase: high protein required")

        elif req.age < 45:
            base["soybean_meal"] += 3
            notes.append("Grower phase adjustment")

    elif req.animal == "cow":
        base["wheat_bran"] += 5
        base["corn"] -= 3
        notes.append("Ruminant fiber optimization")

    elif req.animal == "sheep":
        base["wheat_bran"] += 4
        notes.append("Sheep fiber-balanced diet")

    # -----------------------
    # Goal logic
    # -----------------------
    if req.goal == "growth":
        base["soybean_meal"] += 4
        base["insect_protein"] += 3
        notes.append("Growth mode active")

    elif req.goal == "cost":
        base["soybean_meal"] -= 3
        base["corn"] += 5
        notes.append("Cost optimization mode")

    # -----------------------
    # Insect protein logic
    # -----------------------
    if "soybean_meal" in req.available:
        base["insect_protein"] += 5
        recommendations.append("Replace part of soybean meal with insect protein")

    # -----------------------
    # Normalize to %
    # -----------------------
    total = sum(base.values())
    for k in base:
        base[k] = round((base[k] / total) * 100, 2)

    result = {
        "animal": req.animal,
        "age": req.age,
        "goal": req.goal,
        "ration": base,
        "notes": notes,
        "recommendations": recommendations,
        "version": "AI Optimize v2"
    }

    # -----------------------
    # SAVE TO DATABASE
    # -----------------------
    record = RationHistory(
        animal=req.animal,
        age=req.age,
        goal=req.goal,
        input_data=req.dict(),
        output_data=result
    )

    db.add(record)
    db.commit()

    return result

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
def root():
    return {"status": "Farm AI is running"}