"""YaMDb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import UserCodeViewSet, MyTokenObtainPairView, UsersViewSet, \
    SpecificUserViewSet, MeUserViewSet, CategoriesViewSet, CategoryViewSet, \
    GenreViewSet, GenresViewSet, TitleViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register('titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='reviews')

urlpatterns = [
    path('auth/email/', UserCodeViewSet.as_view(), name='conformation_code'),
    path('auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('users/me/', MeUserViewSet.as_view()),
    path('users/<str:username>/', SpecificUserViewSet.as_view()),
    path('users/', UsersViewSet.as_view()),
    path('categories/<str:slug>/', CategoryViewSet.as_view()),
    path('categories/', CategoriesViewSet.as_view()),
    path('genres/<str:slug>/', GenreViewSet.as_view()),
    path('genres/', GenresViewSet.as_view()),
    path('', include(router.urls))

]
