from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        new_user = self.model(email=self.normalize_email(email), name=name, **extra_fields)
        new_user.set_password(password)
        new_user.is_active = True
        new_user.save(using=self._db)

        return new_user

    def create_superuser(self, email, password):
        new_user = self.model(email=self.normalize_email(email))
        new_user.set_password(password)
        new_user.is_active = True
        new_user.is_superuser = True
        new_user.is_staff = True
        new_user.save(using=self._db)

        return new_user
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

