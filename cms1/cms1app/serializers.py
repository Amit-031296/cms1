from rest_framework import serializers
from django.contrib.auth.models import User
from cms1app.models import *
import json
import os


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMSAuthorContent
        fields = ['cmsusers', 'content_title','content_body','content_summary','content_file','content_category']

# class ContentUpdateDeleteSerilizer(serializers.ModelSerializer):
    
#     class Meta:
#         model = CMSUsersContent
#         fields = ['id', 'cmsusers','content_title','content_body',\
#             'content_summary','content_file','content_category','user_email']