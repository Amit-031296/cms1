from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from cms1 import views,views1

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('cmsusers/', views.CMSUsersList.as_view()),
    path('contents/', views.CMSUsersContentList.as_view()),
    path('contents/<int:pk>/', views.CMSUsersContentDetail.as_view()),
    path('cms_user_content_view/',views.cms_user_content_view),
    path('cms_user_content_create_view/',views.cms_user_content_create_view)
]

urlpatterns = format_suffix_patterns(urlpatterns)