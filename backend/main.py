from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.gemini_utils import generate_linkedin_post
from backend.auth import auth_router  # Import auth router

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.post("/generate")
def generate_post(length: str, mood: str, language: str):
    return {"post": generate_linkedin_post(mood, length, language)}

@app.get("/")
def read_root():
    return {"message": "Welcome to the content generator API"}
