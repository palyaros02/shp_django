from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name
