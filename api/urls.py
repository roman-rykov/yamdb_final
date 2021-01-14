from django.urls import include, path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (
    CommentModelViewSet,
    ReviewModelViewSet,
    CategoryViewSet,
    GenreViewSet,
)

v1_router = DefaultRouter()
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewModelViewSet,
    'review',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentModelViewSet,
    'comment',
)
v1_router.register(
    'categories',
    CategoryViewSet,
    'categorys',
)
v1_router.register(
    'genres',
    GenreViewSet,
    'genres'
)

urlpatterns = [
    path(
        'v1/api-auth/',
        include('rest_framework.urls', namespace='rest_framework'),
    ),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'v1/',
        include(v1_router.urls),
    ),
]
