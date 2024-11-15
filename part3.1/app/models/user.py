#!/usr/bin/python3

from app.models.base import BaseModel
import re
from app import bcrypt, db

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, first_name: str, last_name: str, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        # self.password = None
        self.hash_password(password)
    
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def validate_name(name: str) -> str:
        if not name or len(name) > 50:
            raise ValueError("Name is required and/or maximum length is of 50 characters")
        return (name)
    
    @staticmethod
    def validate_email(email : str) -> str:
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError("Email is required and/or format is invalid")
        return (email)
    
    def update(self, first_name=None, last_name= None, email= None, password=None, is_admin= None):
        if first_name:
            self.first_name = self.validate_name(first_name)
        if last_name:
            self.last_name = self.validate_name(last_name)
        if email:
            self.email = self.validate_email(email)
        if password:
            self.hash_password(password)
        if is_admin is not None:
            self.is_admin = is_admin
        super().update()