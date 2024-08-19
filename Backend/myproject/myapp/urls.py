from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet, AlbumViewSet, PhotoViewSet, TodoViewSet, LoginView, AddAdminView, AdminUserViewSet, PermissionViewSet, TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'todos', TodoViewSet)
router.register(r'admin-users', AdminUserViewSet, basename='adminuser')
router.register(r'permissions', PermissionViewSet)  # Yeni eklenen izin viewset'i

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('add-admin/', AddAdminView.as_view(), name='add_admin'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]