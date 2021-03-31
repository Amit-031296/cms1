from django.db import models
import re
# from .validators import *
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



# Create your models here.

class CMSAuthor(models.Model):
    email = models.CharField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    # password_val_regex = RegexValidator(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$',message="The Password must have minimum length of 8 characters \
    #      1 UpperCase Letter and 1 Lowercase Letter")
    user_password = models.CharField(max_length=50)
    user_firstname = models.CharField(max_length=50)
    user_lastname = models.CharField(max_length=50)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    user_phone_number = models.CharField(max_length=17)
    user_address = models.TextField(blank=True, default='')
    user_city = models.CharField(max_length=50,blank=True, default='')
    user_state = models.CharField(max_length=50,blank=True, default='')
    user_country = models.CharField(max_length=50,blank=True, default='')
    # pincode_regex = RegexValidator(regex=r'^\d{4}|\d{6}',message="Enter Valid Pincode")
    user_pincode = models.CharField(max_length=6)
    user_role = models.CharField(max_length=6,default = 'Author')

    def __str__(self):
        return self.email


class CMSAuthorContent(models.Model):
    cmsusers = models.ForeignKey(CMSAuthor,on_delete=models.CASCADE)
    content_title = models.CharField(max_length=30)
    content_body = models.CharField(max_length=300)
    content_summary = models.CharField(max_length=60)
    content_file = models.FileField()
    content_category = models.CharField(max_length=60)

    def __str__(self):
        return self.content_title