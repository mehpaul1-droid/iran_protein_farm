from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Farm AI Industrial System",
    version="1.0.0"
)

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production بعداً محدودش می‌کنیم
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
        "message": "Industrial AI API Running"
    }

# ---------------- AI OPTIMIZE ----------------
@app.post("/ai/optimize-ration")
def optimize_ration(req: FeedRequest):
    try:
        # 🔥 نسخه ساده AI (فعلاً rule-based)
        base_score = 100

        if req.animal.lower() == "chicken":
            base_score += 10

        if req.age > 20:
            base_score -= 5

        if "soybean_meal" in req.available:
            base_score += 15

        result = {
            "animal": req.animal,
            "goal": req.goal,
            "score": base_score,
            "recommendation": "Balanced high-protein feed recommended",
            "ingredients": req.available
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))