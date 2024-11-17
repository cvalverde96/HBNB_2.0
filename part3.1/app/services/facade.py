#!/usr/bin/python3

from app.services.repositories.user_repository import UserRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.placeamenity_repository import PlaceAmenityRepository


from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
        self.place_amenity_repo = PlaceAmenityRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user.password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repo.update(user.id, user_data)
        return user

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        return amenity

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        allowed_fields = {'name'}
        for key, value in amenity_data.items():
            if key in allowed_fields:
                setattr(amenity, key, value)

        self.amenity_repo.update(amenity.id, amenity_data)
        return amenity

    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id', None)
        if not owner_id:
            raise ValueError("Owner ID is required.")

        owner = self.get_user(owner_id)
        if not owner:
            raise Exception('Owner not found')

        place = Place(owner_id=owner_id, **place_data)

        self.place_repo.add(place)

        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError('Owner not found')
            place.user_id = owner

        for key, value in place_data.items():
            if key not in ['owner_id']:
                setattr(place, key, value)

        self.place_repo.update(place_id, place_data)
        return place

    def create_review(self, review_data):
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError('Place not found')

        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError('User not found')

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=place.id,
            user_id=user.id
        )

        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_by_attribute('place_id', place_id)
        return [reviews] if isinstance(reviews, Review) else reviews if reviews else []

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            if key in ['text', 'rating']:
                setattr(review, key, value)

        review.validations()

        self.review_repo.update(review.id, review_data)

        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        self.review_repo.delete(review_id)

        return True

    def create_place_amenity(self, amenity_data):

        place_amenity = PlaceAmenity(
            place_id=amenity_data['place_id'],
            amenity_id=amenity_data['amenity_id']
        )

        self.place_amenity_repo.add(place_amenity)

        return place_amenity

    def get_place_amenity(self):
        return self.place_amenity_repo.get_all()

    def get_place_amenity_by_place(self, place_id):
        return self.place_amenity_repo.get_by_attribute('place_id', place_id)
