from api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users',  views.UserViewSet)
router.register(r'userkeys',  views.UserKeyViewSet)
router.register(r'images',  views.ImageViewSet, basename='Images')

urlpatterns = [
    path('', include(router.urls)),
    path('search-user/', views.search_user),
    path('followings/', views.followings),
    path('followers/', views.followers),
    path('follow/', views.follow),
    path('unfollow/', views.unfollow),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]