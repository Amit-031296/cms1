from rest_framework import serializers
from django.contrib.auth.models import User
from cms1.models import *
import json
# from django.core import serializers
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CMSUsersContentSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='cmsusers.user_email')

    class Meta:
        model = CMSUsersContent
        fields = ['id', 'cmsusers','content_title','content_body',\
            'content_summary','content_file','content_category','user_email']

class CMSUsersSerializer(serializers.ModelSerializer):
    contents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = CMSUsers
        fields = ['id', 'email', 'user_password', 'user_firstname', \
            'user_lastname','user_phone_number','user_address','user_city',\
                'user_state','user_country','user_pincode','user_role','contents']

class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = CMSUsers
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
				'password': {'write_only': True},
		}	
        
    def	save(self):
        account = CMSUsers(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account

# class ContentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CMSUsersContent
#         fields = ['content_title','content_body',\
#             'content_summary','content_file']

class ContentSerializer(serializers.Serializer):
    content_title = serializers.CharField(max_length=30)
    content_body = serializers.CharField(max_length=300)
    content_summary = serializers.CharField(max_length=60)
    content_file = serializers.FileField()
    content_category = serializers.CharField(max_length=60)


# def ContentSerializer(contents):
#     data = serializers.serialize('json',contents)
#     return data
#     def dic(self,contents):
#         list1 = list()
#         for i in contents:
#             dic = dict()
#             dic['cmsusers'] = i.cmsusers
#             dic['content_title'] = i.content_title
#             dic['content_body'] = i.content_body
#             dic['content_summary'] = i.content_summary
#             dic['content_file'] = i.content_file
#             dic['content_category'] = i.content_category
#             list1.append(dic)
#         json_posts = json.dumps(list(list1))
#         return json_posts

# class BookListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         print("validated_data =>",validated_data)
#         books = [contents(**item) for item in validated_data]
#         return CMSUsersContent.objects.bulk_create(books)


class ContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMSUsersContent
        fields = ['content_title', 'content_body', 'content_summary', 'content_file', 'content_category','cmsusers']
    
    def save(self):
        try:
            print(self.validated_data)
            print(type(self.validated_data))
            content_title = self.validated_data['content_title']
            content_body = self.validated_data['content_body']
            content_summary = self.validated_data['content_summary']
            content_file = self.validated_data['content_file']
            content_category = self.validated_data['content_category']
            print("content_title =>",content_title)
            print("content_body =>",content_body)
            print("content_summary =>",content_summary)
            print("content_file =>",content_file)
            print("content_category =>",content_category)
            print("type content_category =>",type(content_category))
            cmsusers = self.validated_data['cmsusers']
            content_post = CMSUsersContent(
                cmsusers=cmsusers,
                content_title=content_title,
                content_body=content_body,
                content_summary=content_summary,
                content_file=content_file,
                content_category=content_category
                )
            # url = os.path.join(settings.TEMP , str(content_file))
            # storage = FileSystemStorage(location=url)
            # print("storage",storage)
            # with storage.open('', 'wb+') as destination:
            #     for chunk in content_file.chunks():
            #         destination.write(chunk)
            #     destination.close()
            # os.remove(url)
            content_post.save()
            return content_post
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})

