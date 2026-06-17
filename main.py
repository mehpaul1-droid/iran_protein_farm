from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Farm AI Industrial System",
    version="1.1.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MEMORY DB (TEMP) ----------------
db_history = []

# ---------------- MODEL ----------------
class FeedRequest(BaseModel):
    animal: str
    age: int
    goal: str
    available: Optional[List[str]] = []

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Industrial AI API Running"}

# ---------------- AI OPTIMIZE + SAVE ----------------
@app.post("/ai/optimize-ration")
def optimize_ration(req: FeedRequest):
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
            "timestamp": datetime.now().isoformat()
        }

        # 🔥 SAVE TO HISTORY
        db_history.append(result)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- HISTORY API ----------------
@app.get("/ai/history")
def get_history():
    return {
        "count": len(db_history),
        "data": db_history
    }