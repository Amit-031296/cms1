from rest_framework import serializers
from cms1.models import *

# import os
# from django.conf import settings
# from django.core.files.storage import default_storage
# from django.core.files.storage import FileSystemStorage
# IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
# MIN_TITLE_LENGTH = 5
# MIN_BODY_LENGTH = 50

# from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid


class CMSUsersContentSerializer(serializers.ModelSerializer):

	# username = serializers.SerializerMethodField('get_username_of_content')
	# image 	 = serializers.SerializerMethodField('validate_image_url')

	class Meta:
		model = CMSUsersContent
		fields = ['pk', 'cmsusers', 'content_title', 'content_body', 'content_summary', 'content_file', 'content_category','cmsusers']


	# def get_username_of_content(self, content):
	# 	username = content.cmsusers
	# 	return username

	# def validate_image_url(self, content):
	# 	image = blog_post.image
	# 	new_url = image.url
	# 	if "?" in new_url:
	# 		new_url = image.url[:image.url.rfind("?")]
	# 	return new_url




# class BlogPostUpdateSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = BlogPost
# 		fields = ['title', 'body', 'image']

# 	def validate(self, blog_post):
# 		try:
# 			title = blog_post['title']
# 			if len(title) < MIN_TITLE_LENGTH:
# 				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
# 			body = blog_post['body']
# 			if len(body) < MIN_BODY_LENGTH:
# 				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
# 			image = blog_post['image']
# 			url = os.path.join(settings.TEMP , str(image))
# 			storage = FileSystemStorage(location=url)

# 			with storage.open('', 'wb+') as destination:
# 				for chunk in image.chunks():
# 					destination.write(chunk)
# 				destination.close()

# 			# Check image size
# 			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
# 				os.remove(url)
# 				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

# 			# Check image aspect ratio
# 			if not is_image_aspect_ratio_valid(url):
# 				os.remove(url)
# 				raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

# 			os.remove(url)
# 		except KeyError:
# 			pass
# 		return blog_post


# class BlogPostCreateSerializer(serializers.ModelSerializer):


# 	class Meta:
# 		model = BlogPost
# 		fields = ['title', 'body', 'image', 'date_updated', 'author']


# 	def save(self):
		
# 		try:
# 			image = self.validated_data['image']
# 			title = self.validated_data['title']
# 			if len(title) < MIN_TITLE_LENGTH:
# 				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
# 			body = self.validated_data['body']
# 			if len(body) < MIN_BODY_LENGTH:
# 				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			
# 			blog_post = BlogPost(
# 								author=self.validated_data['author'],
# 								title=title,
# 								body=body,
# 								image=image,
# 								)

# 			url = os.path.join(settings.TEMP , str(image))
# 			storage = FileSystemStorage(location=url)

# 			with storage.open('', 'wb+') as destination:
# 				for chunk in image.chunks():
# 					destination.write(chunk)
# 				destination.close()

# 			# Check image size
# 			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
# 				os.remove(url)
# 				raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

# 			# Check image aspect ratio
# 			if not is_image_aspect_ratio_valid(url):
# 				os.remove(url)
# 				raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

# 			os.remove(url)
# 			blog_post.save()
# 			return blog_post
# 		except KeyError:
# 			raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})