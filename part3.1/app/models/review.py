#!/usr/bin/python3

from app.models.base import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text: str, rating: int, place: "Place", user: "User"):
        super().__init__()
        self.text = self.validate_text(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)
    
    @staticmethod
    def validate_text(text: str) -> str:
        if not text:
            raise ValueError("Text required")
        return (text)
    
    @staticmethod
    def validate_rating(rating: int) -> int:
        if not (1 <= rating <= 5):
            raise ValueError("Rating given to the place, must be between 1 and 5.")
        return (rating)
    
    @staticmethod
    def validate_place(place: "Place") -> "Place":
        if not isinstance(place, Place):
            raise ValueError("Must be a valid Place instance")
        return (place)
    
    @staticmethod
    def validate_user(user: "User") -> "User":
        if not isinstance(user, User):
            raise ValueError("Must be a valid User instance")
        return (user)
    
    def update(self, text: str = None, rating: int = None):
        if text:
            self.text = self.validate_text(text)
        if rating:
            self.rating= self.validate_rating(rating)
        super().update()
    
    def __str__(self):
        return (f"Review(id={self.id}, text={self.text}, rating={self.rating}, "
                f"place={self.place.title}, user={self.user.first_name} {self.user.last_name}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")