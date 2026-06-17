from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import SessionLocal, engine
from models import Base, AIHistory

# ---------------- INIT DB ----------------

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Farm AI Industrial System",
    version="2.1.0"
)

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------

class FeedRequest(BaseModel):
    animal: str
    age: int
    goal: str
    available: Optional[List[str]] = []

# ---------------- ROOT ----------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Industrial AI SaaS API Running"
    }

# ---------------- AI OPTIMIZATION ----------------

@app.post("/ai/optimize-ration")
def optimize_ration(req: FeedRequest):

    db = SessionLocal()

    try:
        score = 100

        if req.animal.lower() == "chicken":
            score += 10

        if req.age > 20:
            score -= 5

        if "soybean_meal" in req.available:
            score += 15

        result = {
            "animal": req.animal,
            "goal": req.goal,
            "score": score,
            "recommendation": "Balanced high-protein feed recommended",
            "ingredients": req.available,
            "timestamp": datetime.utcnow().isoformat()
        }

        record = AIHistory(
            animal=req.animal,
            goal=req.goal,
            score=score,
            ingredients=",".join(req.available)
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()

# ---------------- AI HISTORY ----------------

@app.get("/ai/history")
def get_history():

    db = SessionLocal()

    try:
        records = (
            db.query(AIHistory)
            .order_by(AIHistory.id.desc())
            .all()
        )

        return {
            "count": len(records),
            "data": [
                {
                    "id": r.id,
                    "animal": r.animal,
                    "goal": r.goal,
                    "score": r.score,
                    "ingredients": r.ingredients,
                    "timestamp": r.timestamp
                }
                for r in records
            ]
        }

    finally:
        db.close()

# ---------------- DASHBOARD STATS ----------------

@app.get("/dashboard/stats")
def dashboard_stats():

    db = SessionLocal()

    try:
        records = db.query(AIHistory).all()

        total_requests = len(records)

        average_score = 0

        if total_requests > 0:
            average_score = (
                sum(r.score for r in records)
                / total_requests
            )

        return {
            "total_requests": total_requests,
            "average_score": round(average_score, 1),
            "active_farms": 12
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()