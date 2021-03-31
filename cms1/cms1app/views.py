from django.contrib.auth.models import User
from cms1app.serializers import AuthorSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from cms1app.models import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class RegisterView(generics.ListCreateAPIView):
    queryset = CMSAuthorContent.objects.all()
    serializer_class = AuthorSerializer

class ContentUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = CMSAuthorContent.objects.all()
    serializer_class = AuthorSerializer