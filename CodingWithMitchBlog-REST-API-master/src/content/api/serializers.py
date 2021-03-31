from rest_framework import serializers
from content.models import CMSAuthorContent

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
FILE_SIZE_MAX_BYTES = 1024 * 1024 * 10 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from blog.utils import is_image_aspect_ratio_valid, is_image_size_valid


class ContentSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')
	content_file_pdf 	 = serializers.SerializerMethodField('validate_file_url')

	class Meta:
		model = CMSAuthorContent
		fields = ['pk', 'content_title', 'slug', 'content_body','content_summary', 'content_file_pdf','content_category', 'date_updated', 'username']


	def get_username_from_author(self, content):
		username = content.author.username
		return username

	def validate_file_url(self, content):
		content = content.content_file_pdf
		new_url = content.url
		if "?" in new_url:
			new_url = content.url[:content.url.rfind("?")]
		return new_url




class ContentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMSAuthorContent
        fields = ['content_title', 'content_body','content_summary', 'content_file_pdf','content_category', 'date_updated', 'author']
        
    def validate(self, content):
        try:
            content_title = content['content_title']
            if len(content_title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
                
            content_body = content['content_body']
            if len(content_body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
                
            content_file_pdf = content['content_file_pdf']
            content_summary = content['content_summary']
            content_category = content['content_category']
            url = os.path.join(settings.TEMP , str(content_file_pdf))
            storage = FileSystemStorage(location=url)
            
            with storage.open('', 'wb+') as destination:
                for chunk in content_file_pdf.chunks():
                    destination.write(chunk)
                destination.close()
                
            if not is_image_size_valid(url, FILE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError({"response": "That pdf is too large. Images must be less than 10 MB. Try a different pdf."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})
            os.remove(url)
            
        except KeyError:
            pass
        return content


class ContentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMSAuthorContent
        fields = ['content_title', 'content_body','content_summary', 'content_file_pdf','content_category', 'date_updated', 'author']
    
    def save(self):
        try:
            content_file_pdf = self.validated_data['content_file_pdf']
            content_title = self.validated_data['content_title']
            if len(content_title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
            content_body = self.validated_data['content_body']
            if len(content_body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
            content_summary = self.validated_data['content_summary']
            content_category = self.validated_data['content_category']
            content = CMSAuthorContent(
								author=self.validated_data['author'],
								content_title=content_title,
								content_body=content_body,
                                content_summary=content_summary,
								content_file_pdf=content_file_pdf,
                                content_category=content_category
								)
                                
            url = os.path.join(settings.TEMP , str(content_file_pdf))
            storage = FileSystemStorage(location=url)
            
            with storage.open('', 'wb+') as destination:
                for chunk in content_file_pdf.chunks():
                    destination.write(chunk)
                destination.close()
                
            if not is_image_size_valid(url, FILE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError({"response": "That pdf is too large. Images must be less than 10 MB. Try a different pdf."})

			# Check image aspect ratio
			# if not is_image_aspect_ratio_valid(url):
			# 	os.remove(url)
			# 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})
            os.remove(url)
            content.save()
            return content
        except KeyError:
            raise serializers.ValidationError({"response": "You must have a title, some content, and an file."})









