from django.db import models
from django.conf import settings
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

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    time_required = models.IntegerField()
    link = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return str(self.id) + " - " + self.title

class Tag(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name