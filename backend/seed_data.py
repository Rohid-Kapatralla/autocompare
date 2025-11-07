import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

sample_cars = [
    {
        "id": "car1",
        "make": "Tesla",
        "model": "Model S",
        "year": 2024,
        "price": 74990,
        "type": "Sedan",
        "image": "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=800&q=80",
        "specs": {
            "engine": "Dual Motor AWD",
            "horsepower": "670 hp",
            "transmission": "Automatic",
            "range": "405 miles",
            "acceleration": "3.1s 0-60mph"
        },
        "features": ["Autopilot", "Premium Interior", "Glass Roof", "22\" Wheels", "Full Self-Driving Capability"],
        "description": "Premium electric sedan with exceptional performance and cutting-edge technology."
    },
    {
        "id": "car2",
        "make": "BMW",
        "model": "X5",
        "year": 2024,
        "price": 63700,
        "type": "SUV",
        "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
        "specs": {
            "engine": "3.0L Inline-6 Turbo",
            "horsepower": "335 hp",
            "transmission": "8-Speed Automatic",
            "fuel_economy": "21/26 MPG",
            "drivetrain": "AWD"
        },
        "features": ["Panoramic Sunroof", "Leather Seats", "Apple CarPlay", "Adaptive Cruise Control", "360° Camera"],
        "description": "Luxury SUV combining performance, comfort, and advanced technology."
    },
    {
        "id": "car3",
        "make": "Mercedes-Benz",
        "model": "C-Class",
        "year": 2024,
        "price": 45000,
        "type": "Sedan",
        "image": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80",
        "specs": {
            "engine": "2.0L Inline-4 Turbo",
            "horsepower": "255 hp",
            "transmission": "9-Speed Automatic",
            "fuel_economy": "25/34 MPG",
            "drivetrain": "RWD"
        },
        "features": ["MBUX Infotainment", "LED Headlights", "Heated Seats", "Wireless Charging", "Ambient Lighting"],
        "description": "Elegant sedan with refined styling and premium comfort features."
    },
    {
        "id": "car4",
        "make": "Audi",
        "model": "Q7",
        "year": 2024,
        "price": 59800,
        "type": "SUV",
        "image": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80",
        "specs": {
            "engine": "3.0L V6 Turbo",
            "horsepower": "335 hp",
            "transmission": "8-Speed Automatic",
            "fuel_economy": "19/24 MPG",
            "drivetrain": "Quattro AWD"
        },
        "features": ["Virtual Cockpit", "3-Row Seating", "Bang & Olufsen Sound", "Matrix LED Lights", "Air Suspension"],
        "description": "Spacious luxury SUV with advanced technology and versatile seating."
    },
    {
        "id": "car5",
        "make": "Porsche",
        "model": "911",
        "year": 2024,
        "price": 106100,
        "type": "Coupe",
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80",
        "specs": {
            "engine": "3.0L Twin-Turbo Flat-6",
            "horsepower": "379 hp",
            "transmission": "8-Speed PDK",
            "acceleration": "4.0s 0-60mph",
            "top_speed": "182 mph"
        },
        "features": ["Sport Chrono Package", "Active Suspension", "Porsche Communication", "Sports Exhaust", "Launch Control"],
        "description": "Iconic sports car delivering thrilling performance and timeless design."
    },
    {
        "id": "car6",
        "make": "Ford",
        "model": "Mustang",
        "year": 2024,
        "price": 28000,
        "type": "Coupe",
        "image": "https://images.unsplash.com/photo-1584345604476-8ec5f2f62d0f?w=800&q=80",
        "specs": {
            "engine": "2.3L EcoBoost Turbo",
            "horsepower": "310 hp",
            "transmission": "6-Speed Manual",
            "fuel_economy": "21/32 MPG",
            "drivetrain": "RWD"
        },
        "features": ["SYNC 4 Infotainment", "Performance Package", "Active Exhaust", "Track Apps", "Recaro Seats"],
        "description": "American muscle car with bold styling and exhilarating performance."
    },
    {
        "id": "car7",
        "make": "Toyota",
        "model": "Camry",
        "year": 2024,
        "price": 26420,
        "type": "Sedan",
        "image": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&q=80",
        "specs": {
            "engine": "2.5L 4-Cylinder",
            "horsepower": "203 hp",
            "transmission": "8-Speed Automatic",
            "fuel_economy": "28/39 MPG",
            "drivetrain": "FWD"
        },
        "features": ["Toyota Safety Sense", "Apple CarPlay", "Dual-Zone Climate", "Blind Spot Monitor", "Adaptive Cruise"],
        "description": "Reliable sedan with excellent fuel efficiency and modern features."
    },
    {
        "id": "car8",
        "make": "Honda",
        "model": "CR-V",
        "year": 2024,
        "price": 30000,
        "type": "SUV",
        "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&q=80",
        "specs": {
            "engine": "1.5L Turbo 4-Cylinder",
            "horsepower": "190 hp",
            "transmission": "CVT",
            "fuel_economy": "28/34 MPG",
            "drivetrain": "AWD"
        },
        "features": ["Honda Sensing", "Panoramic Sunroof", "Hands-Free Liftgate", "Wireless Charging", "Remote Start"],
        "description": "Versatile compact SUV perfect for families with excellent safety ratings."
    },
    {
        "id": "car9",
        "make": "Lexus",
        "model": "RX 350",
        "year": 2024,
        "price": 48550,
        "type": "SUV",
        "image": "https://images.unsplash.com/photo-1613909207039-6b173b755cc1?w=800&q=80",
        "specs": {
            "engine": "3.5L V6",
            "horsepower": "295 hp",
            "transmission": "8-Speed Automatic",
            "fuel_economy": "20/27 MPG",
            "drivetrain": "AWD"
        },
        "features": ["Mark Levinson Audio", "Panoramic View Monitor", "Heated/Ventilated Seats", "Head-Up Display", "Power Liftgate"],
        "description": "Premium SUV offering exceptional comfort and refined luxury experience."
    },
    {
        "id": "car10",
        "make": "Chevrolet",
        "model": "Silverado",
        "year": 2024,
        "price": 36000,
        "type": "Truck",
        "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80",
        "specs": {
            "engine": "5.3L V8",
            "horsepower": "355 hp",
            "transmission": "10-Speed Automatic",
            "towing_capacity": "11,500 lbs",
            "drivetrain": "4WD"
        },
        "features": ["Multi-Flex Tailgate", "Trailering Package", "Bed Liner", "Teen Driver Mode", "Wireless CarPlay"],
        "description": "Powerful full-size truck built for work and adventure with impressive capability."
    },
    {
        "id": "car11",
        "make": "Volkswagen",
        "model": "Golf GTI",
        "year": 2024,
        "price": 31000,
        "type": "Hatchback",
        "image": "https://images.unsplash.com/photo-1552519507-cf6e7c2755ff?w=800&q=80",
        "specs": {
            "engine": "2.0L Turbo 4-Cylinder",
            "horsepower": "241 hp",
            "transmission": "6-Speed Manual",
            "fuel_economy": "24/32 MPG",
            "drivetrain": "FWD"
        },
        "features": ["Digital Cockpit", "Plaid Seats", "Adaptive Dampers", "LED Lighting", "Performance Brakes"],
        "description": "Fun and practical hot hatch with impressive handling and everyday usability."
    },
    {
        "id": "car12",
        "make": "Mazda",
        "model": "CX-5",
        "year": 2024,
        "price": 28500,
        "type": "SUV",
        "image": "https://images.unsplash.com/photo-1600705722908-bab1ca4701e1?w=800&q=80",
        "specs": {
            "engine": "2.5L 4-Cylinder",
            "horsepower": "187 hp",
            "transmission": "6-Speed Automatic",
            "fuel_economy": "25/31 MPG",
            "drivetrain": "AWD"
        },
        "features": ["i-ACTIVSENSE Safety", "Bose Sound System", "Power Liftgate", "Heated Steering Wheel", "Traffic Sign Recognition"],
        "description": "Stylish compact SUV with engaging driving dynamics and upscale interior."
    }
]

async def seed_database():
    # Clear existing cars
    await db.cars.delete_many({})
    
    # Insert sample cars
    if sample_cars:
        await db.cars.insert_many(sample_cars)
        print(f"Seeded {len(sample_cars)} cars into the database")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())

