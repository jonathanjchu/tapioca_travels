from django.db import models
from apps.users.models import *

# Create your models here.

TRANSPORTATION_MODE = (
    (0, "Airplane"),
    (1, "Personal Car"),
    (2, "Bus"),
    (3, "Train"),
    (4, "Foot"),
    (5, "Subway"),
    (6, "Cab")
)


ACCOMODATION_TYPE = (
    (0, "Hotel"),
    (1, "Hostel"),
    (2, "Air BnB"),
    (3, "Couchsurfing"),
    (4, "Camping"),
    (5, "Streets"),
    (6, "Private Home")
)


class TripManager(models.Manager):
    def validate(self, form):
        errors = {}

        if len(form['name']) < 1:
            errors['name'] = "Please name your trip"
        
        if len(form['trip_start']) < 1:
            errors['trip_start'] = "Please select a start date"
    
        if len(form['trip_end']) < 1:
            errors['trip_end'] = "Please select an end date"

        return errors


class LocationManager(models.Manager):
    def validate(self, form):
        errors = {}

        if len(form['name']) < 1:
            errors['name'] = "Please enter a location name"
        
        # if len(form['desc']) < 1:
        #     errors['desc'] = "Please enter a description"

        return errors


class Location(models.Model):
    name = models.CharField(max_length=64)
    location_type = models.CharField(max_length=64)
    info = models.TextField(max_length=1024)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    fees = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by_user = models.ForeignKey(User, models.CASCADE, "locations_added")
    parent_location = models.ForeignKey("self", models.CASCADE, "child_locations", blank=True, null=True)
    objects = LocationManager()

    def __repr__(self):
        return f"<Location object: {self.id}:{self.name} ({self.start_time} - {self.end_time})>"

    
    def __lt__(self, other):
        return self.id < other.id
    

    def __gt__(self, other):
        return self.id > other.id


class LocationPicture(models.Model):
    image_name = models.CharField(max_length=64)
    picture_of = models.ForeignKey(Location, models.CASCADE, "picture")
    uploaded_by = models.ForeignKey(User, models.CASCADE, "user_loc_images")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Trip(models.Model):
    name = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    is_private = models.BooleanField()
    created_by = models.ForeignKey(User, models.CASCADE, "trips_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    itinerary = models.ManyToManyField(Location, "part_of_trip")
    companions = models.ManyToManyField(User, "going_on_trip")
    objects = TripManager()

    def __repr__(self):
        return f"<Trip object: {self.id}:{self.name} ({self.start_date - self.end_date})>"



class TripJoinRequest(models.Model):
    trip = models.ForeignKey(Trip, models.CASCADE, "requests_to_join")
    requested_by = models.ForeignKey(User, models.CASCADE, "requesting_to_join")
    is_pending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<TripJoinRequest objects: {self.requested_by.username} wants to join {self.trip.id}>"



class Accomodations(models.Model):
    business_name = models.CharField(max_length=32)
    accomodation_type = models.IntegerField(choices=ACCOMODATION_TYPE)
    address = models.CharField(max_length=255, blank=True)
    price_per_night =  models.FloatField(default=0)
    check_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, models.CASCADE, "accomodations_added")
    trip = models.ForeignKey(Trip, models.CASCADE, "accomodations")


    
class Transportation(models.Model):
    mode = models.IntegerField(choices=TRANSPORTATION_MODE)
    company_name = models.CharField(max_length=32)
    price = models.FloatField()
    origin = models.CharField(max_length=64, blank=True)
    destination = models.CharField(max_length=64, blank=True)
    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, models.CASCADE, "transportation_added")
    trip = models.ForeignKey(Trip, models.CASCADE, "transportations")