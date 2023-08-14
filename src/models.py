from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from api import db

class FoodTruck(db.Model):
    __tablename__ = 'food truck'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(50))
    block = Column(String(50))
    distance = Column(float)
    food_items = Column(String(250))
    latitude = Column(float)
    longitude = Column(float)
    location_description = Column(String(250))
    locationid = Column(Integer)
    opening_hours = Column(String(250))
    zip_codes = Column(String(250))
    lot = Column(String(50))
    facility_type = Column(String(50))

    def __str__(self):
        return self.name