from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.apps import apps
from django.utils import timezone
#  thrid party module
from django_countries.fields import CountryField
from rest_framework_simplejwt.tokens import RefreshToken 

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}



class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)

        # may have to add 'using=self._db' parameter.
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user


class AccountProfileModel(models.Model):
    # user = models.OneToOneField(to=Account, on_delete=models.CASCADE, related_name='profile',)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40,  blank=True)
    gender = models.CharField(max_length=6, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), blank=True, null=True)
    dob = models.DateField(auto_now_add=True)
    
    profile_pic = models.ImageField(null=True, blank=True)
    default_banner =  models.ImageField(default='default/BannerImg.svg')
    banner_pic = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    country_code = models.CharField(max_length=10, default='India')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    
    class Meta:
        abstract = True

 
class Account(AbstractUser, AccountProfileModel):
    '''Account model'''

    userid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, blank=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    otp = models.CharField(max_length=6, validators=[MinLengthValidator(6)], default=None, null=True, blank=True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    can_reset_password = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email')
    )
    username = models.CharField(max_length=40, unique=True, null=True,)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-date_joined']
        verbose_name = "account"     
        verbose_name_plural = "All users"     


    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def token(self):
        token =RefreshToken.for_user(Account)
        return {
            'token': token
        }
        
    def edit_url(self):
        token = RefreshToken.for_user(Account)
        return {
            'token': token
        }
    
class AccountAddress(models.Model):
    #Address fields are here
    address_of = models.OneToOneField(Account, related_name='address_of', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50,  blank=True)
    state = models.CharField(max_length=100, blank=True, )
    country = CountryField(default='India')
    zip = models.CharField(max_length=100, blank=True)

 
 
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        RefreshToken.for_user(Account)

