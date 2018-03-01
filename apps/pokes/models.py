from __future__ import unicode_literals
from django.db import models
import re   #regular expressions

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        if len(postData['firstName']) < 3:
            errors['firstName'] = "First name must be at least 3 characters long"
        if len(postData['lastName']) < 3:
            errors['lastName'] = "Last name must be at least 3 characters long"
        if len(postData['username']) < 2:
            errors['username'] = "Username must be at least 2 characters long"
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email must be of correct format."
        if len(postData['password']) < 6:
            errors['password'] = "Password must be at least 6 characters long"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Password must match password confirmation field"
        return errors

# Models
class User(models.Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):                                                         #method used for debugging, can omit.
        return "<User object: {} {} {}>".format(self.firstName, self.lastName, self.username) 

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name = "pokees")
    pokee = models.ForeignKey(User, related_name = "pokers")
    pokeCount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):                                                         #method used for debugging, can omit.
        return "<Poke object: {} {}>".format(self.poker.username, self.pokee.username) 
