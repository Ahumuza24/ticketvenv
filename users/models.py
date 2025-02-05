from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
