from django.db import models
from django.contrib.auth.models import User
     
class UserProfile(models.Model):
    avatar = models.CharField(max_length=255)
    realname = models.CharField(max_length=100)
    user = models.ForeignKey(User, unique=True)
    
