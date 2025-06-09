from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from psycopg2 import pool
import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

# Logging setup
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# JWT secret key
SECRET_KEY = "22052353"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# PostgreSQL connection pool
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
    logger.error(f"Database connection pool initialization failed: {e}")
    raise

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_connection():
    connection = db_pool.getconn()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection error")
    try:
        yield connection
    finally:
        db_pool.putconn(connection)

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Models
class User(BaseModel):
    username: str
    password: str

# Router instance
auth_router = APIRouter()

# Create user endpoint
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
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        raise HTTPException(status_code=400, detail="User already exists or database error")
    return {"message": "User created successfully"}

# Generate JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token endpoint
@auth_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_connection)):
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, password FROM users WHERE username = %s",
                (form_data.username,),
            )
            user = cursor.fetchone()

        if not user or not pwd_context.verify(form_data.password, user[1]):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Protected endpoint
@auth_router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"message": f"Hello, {username}"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
