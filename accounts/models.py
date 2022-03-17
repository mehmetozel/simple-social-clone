from django.db import models
from django.contrib import auth
# Create your models here.

class User(auth.models.User,auth.models.PermissionsMixin):  #PermissionsMixin allows you to make that view only accessible by logged in users


    def __str__(self):
        return "@{}".format(self.username)