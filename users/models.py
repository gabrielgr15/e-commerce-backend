from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class UserVerificationModel(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification token for {self.user.username}"