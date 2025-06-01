from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.gemini_utils import generate_linkedin_post

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostRequest(BaseModel):
    topic: str
    length: str  # e.g., "short", "medium", "long"
    mood: str    # e.g., "inspirational", "funny", "serious"
    language: str  # e.g., "English", "Hindi"

@app.post("/generate")
def generate_post(req: PostRequest):
    return {"post": generate_linkedin_post(req.topic, req.length, req.mood, req.language)}
 
@app.get("/")
def read_root():
    return{"message": "welcome to the content generator ap"}