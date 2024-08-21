from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User as AdminUser, Permission
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address, Geo, Company, Post, Comment, Album, Photo, Todo, User
from .serializers import UserSerializer, PostSerializer, CommentSerializer, AlbumSerializer, PhotoSerializer, TodoSerializer, AdminUserSerializer, PermissionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Permission


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        if isinstance(request.data, list):
            serializer = UserSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Expected a list of items."}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
      
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        posts = request.data
        serializer = PostSerializer(data=posts, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get_queryset(self):
        user_id = self.request.query_params.get('userId', None)
        if user_id:
            return Post.objects.filter(userId=user_id)
        return Post.objects.all()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        comments = request.data
        serializer = CommentSerializer(data=comments, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post', None)
        if post_id:
            return Comment.objects.filter(postId=post_id)
        return Comment.objects.all()


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = []

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        albums = request.data
        serializer = AlbumSerializer(data=albums, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        if user_id:
            return Album.objects.filter(userId=user_id)
        return Album.objects.all()

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = []

    def get_queryset(self):
        album_id = self.request.query_params.get('album', None)
        if album_id is not None:
            return Photo.objects.filter(album_id=album_id)
        return Photo.objects.all()

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        photos = request.data
        if isinstance(photos, list):
            for photo in photos:
                if 'albumId' not in photo:
                    return Response({'detail': 'albumId is required.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PhotoSerializer(data=photos, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Invalid data. Expected a list.'}, status=status.HTTP_400_BAD_REQUEST)



class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = []

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        todos = request.data
        serializer = TodoSerializer(data=todos, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user', None)
        if user_id:
            return Todo.objects.filter(userId=user_id)
        return Todo.objects.all()


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = []  

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def create(self, request, *args, **kwargs):
        data = request.data
        permissions = data.pop('permissions', [])
        user = AdminUser.objects.create_user(**data)
        user.is_staff = True
        user.save()

        if permissions:
            perms = Permission.objects.filter(codename__in=permissions)
            user.user_permissions.set(perms)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_permission(self, request, pk=None):
        user = self.get_object()
        permission = Permission.objects.get(pk=request.data['permission_id'])
        user.user_permissions.add(permission)
        return Response({'status': 'permission added'})
    
    @action(detail=True, methods=['post'])
    def add_all_permissions(self, request, pk=None):
        user = self.get_object()
        permissions = Permission.objects.all()  
        user.user_permissions.set(permissions)  
        return Response({'status': 'all permissions added'})

    @action(detail=True, methods=['post'])
    def remove_permission(self, request, pk=None):
        user = self.get_object()
        permission = Permission.objects.get(pk=request.data['permission_id'])
        user.user_permissions.remove(permission)
        return Response({'status': 'permission removed'})
    
    
class LoginView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.is_staff:
                refresh = RefreshToken.for_user(user)
                
              
                user_permissions = user.user_permissions.all()
                permissions = [perm.codename for perm in user_permissions]

                
                access_token = refresh.access_token
                access_token['permissions'] = permissions

                return Response({
                    'refresh': str(refresh),
                    'access': str(access_token),
                })
            else:
                return Response({'detail': 'User is not active or not an admin.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class AddAdminView(APIView):
    permission_required = 'add_admin'
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
