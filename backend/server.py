from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class Car(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    make: str
    model: str
    year: int
    price: float
    type: str  # SUV, Sedan, Coupe, etc.
    image: str
    specs: dict  # engine, horsepower, transmission, etc.
    features: List[str]
    description: str

class CarCreate(BaseModel):
    make: str
    model: str
    year: int
    price: float
    type: str
    image: str
    specs: dict
    features: List[str]
    description: str

class TestDrive(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    car_id: str
    user_name: str
    user_email: EmailStr
    user_phone: str
    preferred_date: str
    preferred_time: str
    location: str
    status: str = "pending"  # pending, confirmed, completed, cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TestDriveCreate(BaseModel):
    car_id: str
    user_name: str
    user_email: EmailStr
    user_phone: str
    preferred_date: str
    preferred_time: str
    location: str

class Location(BaseModel):
    id: str
    name: str
    address: str
    city: str
    phone: str


# Routes
@api_router.get("/")
async def root():
    return {"message": "Car Comparison & Test Drive API"}

@api_router.get("/cars", response_model=List[Car])
async def get_cars(
    make: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    year: Optional[int] = Query(None)
):
    query = {}
    
    if make:
        query["make"] = make
    if type:
        query["type"] = type
    if year:
        query["year"] = year
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
    
    cars = await db.cars.find(query, {"_id": 0}).to_list(1000)
    return cars

@api_router.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: str):
    car = await db.cars.find_one({"id": car_id}, {"_id": 0})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@api_router.post("/cars", response_model=Car)
async def create_car(car_input: CarCreate):
    car_dict = car_input.model_dump()
    car_obj = Car(**car_dict)
    doc = car_obj.model_dump()
    
    await db.cars.insert_one(doc)
    return car_obj

@api_router.get("/makes")
async def get_makes():
    makes = await db.cars.distinct("make")
    return {"makes": sorted(makes)}

@api_router.get("/types")
async def get_types():
    types = await db.cars.distinct("type")
    return {"types": sorted(types)}

@api_router.post("/test-drive", response_model=TestDrive)
async def book_test_drive(booking_input: TestDriveCreate):
    # Check if car exists
    car = await db.cars.find_one({"id": booking_input.car_id}, {"_id": 0})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    booking_dict = booking_input.model_dump()
    booking_obj = TestDrive(**booking_dict)
    
    doc = booking_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    
    await db.test_drives.insert_one(doc)
    return booking_obj

@api_router.get("/test-drive", response_model=List[TestDrive])
async def get_test_drives():
    bookings = await db.test_drives.find({}, {"_id": 0}).to_list(1000)
    
    for booking in bookings:
        if isinstance(booking['created_at'], str):
            booking['created_at'] = datetime.fromisoformat(booking['created_at'])
    
    return bookings

@api_router.get("/locations", response_model=List[Location])
async def get_locations():
    locations = [
        {
            "id": "loc1",
            "name": "Downtown Showroom",
            "address": "123 Main Street",
            "city": "New York",
            "phone": "+1 (555) 123-4567"
        },
        {
            "id": "loc2",
            "name": "Westside Auto Center",
            "address": "456 West Avenue",
            "city": "Los Angeles",
            "phone": "+1 (555) 234-5678"
        },
        {
            "id": "loc3",
            "name": "North Point Dealership",
            "address": "789 North Road",
            "city": "Chicago",
            "phone": "+1 (555) 345-6789"
        },
        {
            "id": "loc4",
            "name": "South Bay Motors",
            "address": "321 South Boulevard",
            "city": "Miami",
            "phone": "+1 (555) 456-7890"
        }
    ]
    return locations


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

