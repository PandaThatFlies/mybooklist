from django.db import models

# Create your models here.

class UserProfile(models.Model):
   user_id=models.IntegerField(unique=True)
   book_list=models.TextField()