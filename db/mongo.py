from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.patient_model import Patient
from models.consultations_model import Consultation
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.get_default_database(), document_models=[Patient, Consultation])
