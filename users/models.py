from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    # https://youtu.be/kzN_VCFG9NM (53:00) annotate

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

