from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentModelViewSet, ReviewModelViewSet

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewModelViewSet,
    'review',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentModelViewSet,
    'comment',
)

urlpatterns = [
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework'),
    ),
    path(
        'api-token-auth/',
        obtain_auth_token,
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        '',
        include(router.urls),
    ),
]
