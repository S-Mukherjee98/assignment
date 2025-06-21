from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, age, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, age=age)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, age, password):
        user = self.create_user(email, name, age, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    token_version = models.IntegerField(default=0) 

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age']

    def __str__(self):
        return self.email
