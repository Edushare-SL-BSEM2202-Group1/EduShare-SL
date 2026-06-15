from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routes import resources

# Generate tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduShare API")

# 1. Enable CORS doors first
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="EduShare API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your HTML file to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Mount static folder for file access
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 3. Include API endpoints
app.include_router(resources.router)

@app.get("/")
def root():
    return {"message": "Welcome to the EduShare API!"}