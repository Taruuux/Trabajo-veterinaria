from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import owners, pets, appointments
from dotenv import load_dotenv
import os


load_dotenv()


app = FastAPI(title="VetClinic API")


origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Create tables (simple auto-migrate for MVP)
Base.metadata.create_all(bind=engine)


app.include_router(owners.router)
app.include_router(pets.router)
app.include_router(appointments.router)