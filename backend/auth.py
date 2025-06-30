from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from psycopg2 import pool
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = "22052353"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=5,
        user="postgres",
        password="22052353",
        host="localhost",
        port="5432",
        database="postgenerator"
    )
except Exception as e:
    raise Exception(f"Database connection failed: {e}")

def get_db_connection():
    connection = db_pool.getconn()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection error")
    try:
        yield connection
    finally:
        db_pool.putconn(connection)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class User(BaseModel):
    username: str
    password: str

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: User, db=Depends(get_db_connection)):
    hashed_password = pwd_context.hash(user.password)
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (user.username, hashed_password),
            )
            db.commit()
    except Exception:
        raise HTTPException(status_code=400, detail="User already exists.")
    return {"message": "User signed up successfully"}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@auth_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_connection)):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (form_data.username,))
        user = cursor.fetchone()

    if not user or not pwd_context.verify(form_data.password, user[1]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}
