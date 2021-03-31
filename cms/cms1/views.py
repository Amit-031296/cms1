from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from cms1 import serializers
from django.contrib.auth.models import User
from cms1.models import *
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import BasePermission,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from cms1.validators import *
from django.http import  JsonResponse
import json
User = get_user_model()

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'




class UserList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class CMSUsersContentList(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = CMSUsersContent.objects.all()
    serializer_class = serializers.CMSUsersContentSerializer

    # def perform_create(self, serializer):
    #     serializer.save(cmsusers=self.request.user)

class CMSUsersContentDetail(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = CMSUsersContent.objects.all()
    serializer_class = serializers.CMSUsersContentSerializer


class CMSUsersList(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = CMSUsers.objects.all()
    serializer_class = serializers.CMSUsersSerializer

    # def perform_create(self, serializer):
    #     serializer.save(cmsusers=self.request.user)



class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

        
		serializer = serializers.RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

def validate_email(email):
    cmsusers = None
    try:
        cmsusers = CMSUsers.objects.get(email=email)
    except CMSUsers.DoesNotExist:
        return None
    if cmsusers != None:
        if email_val(email) != None:
            return email
        else:
            return None

def validate_username(username):
	cmsusers = None
	try:
		cmsusers = CMSUsers.objects.get(username=username)
	except CMSUsers.DoesNotExist:
		return None
	if cmsusers != None:
		return username

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def cms_user_content_view(request,):
    if request.method == 'GET':
        contents = CMSUsersContent.objects.filter(cmsusers__email__contains=request.user)
        print("contents =>",contents)
        serializer = serializers.ContentSerializer(contents, many=True)
        # json_posts = json.dumps(list(contents))
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def cms_user_content_create_view(request):
    if request.method == 'POST':
        data = request.data
        data['cmsusers'] = request.user.pk
        print("data ==>",data)
        serializer = serializers.ContentCreateSerializer(data=data)
        data = {}
        if serializer.is_valid():
            content_post = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = content_post.pk
            data['content_title'] = content_post.content_title
            data['content_body'] = content_post.content_body
            data['content_summary'] = content_post.content_summary
            data['content_file'] = content_post.content_file
            data['content_category'] = content_post.content_category
			# image_url = str(request.build_absolute_uri(blog_post.image.url))
			# if "?" in image_url:
			# 	image_url = image_url[:image_url.rfind("?")]
			# data['image'] = image_url
			# data['username'] = content_post.author
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT',])
# @permission_classes((IsAuthenticated,))
# def cms_user_content_update_view(request):

# 	try:
# 		blog_post = BlogPost.objects.get(slug=slug)
# 	except BlogPost.DoesNotExist:
# 		return Response(status=status.HTTP_404_NOT_FOUND)

# 	user = request.user
# 	if blog_post.author != user:
# 		return Response({'response':"You don't have permission to edit that."}) 
		
# 	if request.method == 'PUT':
# 		serializer = BlogPostUpdateSerializer(blog_post, data=request.data, partial=True)
# 		data = {}
# 		if serializer.is_valid():
# 			serializer.save()
# 			data['response'] = UPDATE_SUCCESS
# 			data['pk'] = blog_post.pk
# 			data['title'] = blog_post.title
# 			data['body'] = blog_post.body
# 			data['slug'] = blog_post.slug
# 			data['date_updated'] = blog_post.date_updated
# 			image_url = str(request.build_absolute_uri(blog_post.image.url))
# 			if "?" in image_url:
# 				image_url = image_url[:image_url.rfind("?")]
# 			data['image'] = image_url
# 			data['username'] = blog_post.author.username
# 			return Response(data=data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)