from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class profile(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fullname=models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self):
        return self.username
    

