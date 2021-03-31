from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from cms1app import views

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('register/', views.RegisterView.as_view()),
    path('content_update_delete/<int:pk>', views.ContentUpdateDelete.as_view())
]