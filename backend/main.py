from fastapi import FastAPI
from pydantic import BaseModel
from utils.gemini_utils import generate_linkedin_post
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class PostRequest(BaseModel):
    length: str
    mood: str
    language: str

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate_post(request: PostRequest):
    return {
        "post": generate_linkedin_post(
            request.mood, request.length, request.language
        )
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the LinkedIn Post Generator API"}