from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'



