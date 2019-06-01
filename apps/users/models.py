from django.db import models
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def validator(self, form):
        errors = {}

        if len(form['first_name']) < 1:
            errors['first_name'] = "First Name cannot be blank"
        elif len(form['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"

        if len(form['last_name']) < 1:
            errors['last_name'] = "Last Name cannot be blank"
        elif len(form['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"    

        if len(form['username']) < 1:
            errors['username'] = "Username cannot be blank"
        elif len(form['username']) < 3:
            errors['username'] = "Username must be at least 3 characters"
        elif not form['username'].isalnum():
            errors['username'] = "Only letters and numbers allowed in username"
        else:
            un = User.objects.filter(username=form['username'])
            if len(un) > 0:
                errors['username'] = "Username already in use"

        if len(form['email']) < 1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Email is not valid!"
        else:
            result = User.objects.filter(email=form['email'])
            if len(result) > 0:
                errors['email'] = "Email is already registered"
        
        if len(form['password']) < 1:
            errors['password'] = "Password cannot be blank"
        elif len(form['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters"
        elif form['password'] != form['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=70)
    friends = models.ManyToManyField('self')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User object: {self.first_name} {self.last_name} ({self.email})>"


class Avatar(models.Model):
    image_name = models.CharField(max_length=32, default="default.png")
    user = models.ForeignKey(User, models.CASCADE, "avatar")
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, models.CASCADE, "sent_requests")
    recipient = models.ForeignKey(User, models.CASCADE, "received_requests")
    is_pending = models.BooleanField()

    def __repr__(self):
        return f"<FriendRequest object: {self.sender.username} requested {self.recipient.username}>"

