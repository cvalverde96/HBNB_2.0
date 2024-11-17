from app.models.base import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenity'

    __table_args__ = {'extend_existing': True}

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

        self.amenity_validation()

    def amenity_validation(self):
        if not self.name or len(self.name) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
