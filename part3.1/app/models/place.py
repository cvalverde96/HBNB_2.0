#!/usr/bin/python3

from app.models.base import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title: str, price: float, latitude: float, longitude: float, owner: "User", description: str = None):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.owner_id = self.owner.id
        self.reviews = []
        self.amenities = []
    
    @staticmethod
    def validate_title(title: str) -> str:
        if not title or len(title) > 100:
            raise ValueError("Title is required and/or should be less than or equal to 100 characters.")
        return (title)
    
    @staticmethod
    def validate_price(price: float) -> float:
        if price <= 0:
            raise ValueError("Price must be a positive value.")
        return (price)
    
    @staticmethod
    def validate_latitude(latitude: float) -> float:
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be within the range of -90.0 to 90.0.")
        return (latitude)
    
    @staticmethod
    def validate_longitude(longitude: float) -> float:
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be within the range of -180.0 to 180.0.")
        return (longitude)
    
    @staticmethod
    def validate_owner(owner: "User") -> "User":
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance.")
        return (owner)
    
    
    def add_review(self, review):
        from app.models.review import Review
        if isinstance(review, Review): 
            self.reviews.append(review)
        else:
            raise ValueError("Invalid review object")
    
    def update(self, title: str = None, price: float = None, latitude: float = None, longitude: float = None, description: str = None, owner: "User" = None):
        if title:
            self.title = self.validate_title(title)
        if price:
            self.price = self.validate_price(price)
        if latitude:
            self.latitude = self.validate_latitude(latitude)
        if longitude:
            self.longitude = self.validate_longitude(longitude)
        if description:
            self.description = description
        if owner:
            self.owner = self.validate_owner(owner)
        super().update()
    
    
        def __str__(self):
            return (f"Place(id={self.id}, title={self.title}, description={self.description}, "
                f"price={self.price}, latitude={self.latitude}, longitude={self.longitude}, "
                f"owner={self.owner.first_name} {self.owner.last_name}, created_at={self.created_at}, updated_at={self.updated_at})")

        
        