from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class CustomUser(AbstractUser):
    """Custom user model with unique email field"""

    username = None
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
