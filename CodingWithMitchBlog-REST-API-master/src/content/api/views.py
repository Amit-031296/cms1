from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from account.models import Account
from content.models import CMSAuthorContent
from content.api.serializers import ContentSerializer,ContentCreateSerializer,ContentUpdateSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/blog/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_content_view(request, slug):

	try:
		content = CMSAuthorContent.objects.get(slug=slug)
	except CMSAuthorContent.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = ContentSerializer(content)
		return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/blog/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_content_view(request, slug):
    try:
        content = CMSAuthorContent.objects.get(slug=slug)
    except CMSAuthorContent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    user = request.user
    superuser = user.is_superuser
    print("user ==>",user)
    print("type of user ==>",type(user))
    print("user ==>",user.is_superuser)
    print("user ==>",type(user.is_superuser))
    # if content.author != user:
    #     return Response({'response':"You don't have permission to edit that."}) 
    if superuser==True or content.author == user:
        if request.method == 'PUT':
            serializer = ContentUpdateSerializer(content, data=request.data, partial=True)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data['response'] = UPDATE_SUCCESS
                data['pk'] = content.pk
                data['content_title'] = content.content_title
                data['content_body'] = content.content_body
                data['content_summary'] = content.content_summary
                data['content_category'] = content.content_category
                data['slug'] = content.slug
                data['date_updated'] = content.date_updated
                file_url = str(request.build_absolute_uri(content.content_file_pdf.url))
                if "?" in file_url:
                    file_url = file_url[:file_url.rfind("?")]
                data['content_file_pdf'] = file_url
                data['username'] = content.author.username
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response':"You don't have permission to edit that."})



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_content(request, slug):
	try:
		content = CMSAuthorContent.objects.get(slug=slug)
	except CMSAuthorContent.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if content.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/blog/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_content_view(request, slug):
    try:
        content = CMSAuthorContent.objects.get(slug=slug)
    except CMSAuthorContent.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    user = request.user
    superuser = user.is_superuser
	# if content.author != user:
	# 	return Response({'response':"You don't have permission to delete that."}) 
    if superuser==True or content.author == user:
        if request.method == 'DELETE':
            operation = content.delete()
            data = {}
            if operation:
                data['response'] = DELETE_SUCCESS
            return Response(data=data)
    else:
        return Response({'response':"You don't have permission to delete that."})    


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_content_view(request):
    if request.method == 'POST':
        data = request.data
        print("data ==>",data)
        data['author'] = request.user.pk
        serializer = ContentCreateSerializer(data=data)
        data = {}
        if serializer.is_valid():
            content = serializer.save()
            data['response'] = CREATE_SUCCESS
            data['pk'] = content.pk
            data['content_title'] = content.content_title
            data['content_body'] = content.content_body
            data['content_summary'] = content.content_summary
            # data['content_file_pdf'] = content.content_file_pdf
            data['content_category'] = content.content_category
            data['slug'] = content.slug
            data['date_updated'] = content.date_updated
            file_url = str(request.build_absolute_uri(content.content_file_pdf.url))
            if "?" in file_url:
                file_url = file_url[:file_url.rfind("?")]
            data['content_file_pdf'] = file_url
            data['username'] = content.author.username
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminAuthenticationPermission(permissions.BasePermission):
    # ADMIN_ONLY_AUTH_CLASSES = [rest_framework.authentication.BasicAuthentication, rest_framework.authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/blog/list
#		2) pagination: http://<your-domain>/api/blog/list?page=2
#		3) search: http://<your-domain>/api/blog/list?search=mitch
#		4) ordering: http://<your-domain>/api/blog/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/blog/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiContentListView(ListAPIView):
	queryset = CMSAuthorContent.objects.all()
	serializer_class = ContentSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,AdminAuthenticationPermission)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('content_title', 'content_body', 'author__username')

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_content_of_user_view(request,):

	try:
		content = CMSAuthorContent.objects.filter(author=request.user)
	except CMSAuthorContent.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = ContentSerializer(content,many=True)
		return Response(serializer.data)