from django.db import models
import re
from .validators import *
from django.core.validators import RegexValidator
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

USERROLE_CHOICES = ( 
    ("Admin", "admin"), 
    ("Author", "author")
) 

# class CMSUsers(models.Model):
#     email_val_regex = RegexValidator(regex=r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',message="Enter Valid Email")
#     user_email = models.EmailField(max_length=254, blank=False, unique=True, validators=[email_val_regex])
#     password_val_regex = RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',message="The Password must have minimum length of 8 characters \
#          1 UpperCase Letter and 1 Lowercase Letter")
#     user_password = models.CharField(max_length=50,validators=[password_val_regex])
#     user_firstname = models.CharField(max_length=50)
#     user_lastname = models.CharField(max_length=50)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     user_phone_number = models.CharField(validators=[phone_regex], max_length=17)
#     user_address = models.TextField(blank=True, default='')
#     user_city = models.CharField(max_length=50,blank=True, default='')
#     user_state = models.CharField(max_length=50,blank=True, default='')
#     user_country = models.CharField(max_length=50,blank=True, default='')
#     pincode_regex = RegexValidator(regex=r'^\d{4}|\d{6}',message="Enter Valid Pincode")
#     user_pincode = models.IntegerField(validators=[pincode_regex])
#     user_role = models.CharField(max_length=6,choices = USERROLE_CHOICES)

#     def __str__(self):
#         return self.user_email

class MyCMSUsersManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class CMSUsers(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password_val_regex = RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',message="The Password must have minimum length of 8 characters \
         1 UpperCase Letter and 1 Lowercase Letter")
    user_password = models.CharField(max_length=50,validators=[password_val_regex])
    user_firstname = models.CharField(max_length=50)
    user_lastname = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    user_phone_number = models.CharField(validators=[phone_regex], max_length=17)
    user_address = models.TextField(blank=True, default='')
    user_city = models.CharField(max_length=50,blank=True, default='')
    user_state = models.CharField(max_length=50,blank=True, default='')
    user_country = models.CharField(max_length=50,blank=True, default='')
    pincode_regex = RegexValidator(regex=r'^\d{4}|\d{6}',message="Enter Valid Pincode")
    user_pincode = models.CharField(max_length=6,validators=[pincode_regex])
    user_role = models.CharField(max_length=6,choices = USERROLE_CHOICES,default = 'Admin')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyCMSUsersManager()

    def __str__(self):
        return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

class CMSUsersContent(models.Model):
    cmsusers = models.ForeignKey(CMSUsers, related_name='contents', on_delete=models.CASCADE)
    content_title = models.CharField(max_length=30)
    content_body = models.CharField(max_length=300)
    content_summary = models.CharField(max_length=60)
    content_file = models.FileField()
    content_category = models.CharField(max_length=60)

    def __str__(self):
        return self.content_title

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)