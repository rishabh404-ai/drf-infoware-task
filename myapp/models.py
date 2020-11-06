from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email,photo,username=None, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
      
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name,
            photo=photo,
            username=username
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,photo,username=None,full_name=None, password=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                photo=photo,
                username=username,
                is_staff=True
        )
        return user

    def create_superuser(self, email, photo=None,username=None, full_name=None, password=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                photo=photo,
                username=username,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    username    = models.CharField(max_length=255, blank=True, null=True,unique=True)
    photo       = models.ImageField()
    active      = models.BooleanField(default=True) # can login 
    staff       = models.BooleanField(default=False) # staff user non superuser
    admin       = models.BooleanField(default=False) # superuser 
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email' #username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] 

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_username(self):
        if self.username:
            return self.username
        return self.email        

    def get_photo(self):
        if self.photo:
            return self.photo
        return self.email        

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
         
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def token(sender, instance=None, created=False, **kwargs):
       if created:
           Token.objects.create(user=instance)