from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Cities"


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name}'
    
    class Meta:
        verbose_name_plural = "Countries"


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, user_company=None):
        if not email:
            raise ValueError('Invalid Email')
        if not username:
            raise ValueError('Invalid Username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            user_company=user_company,
        )

        user.set_password(password)  # Set the password
        user.save(using=self._db)  # Save the user to the database
        return user


    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            user_company='company'
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)

        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=50, choices=[("1", "Male"), ("0", "Female")])
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    user_company = models.CharField(max_length=255, default=None, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True,)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", 'first_name', 'last_name',)

    objects = MyAccountManager()

    def __str__(self) -> str:
        return f'{self.email}'
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True