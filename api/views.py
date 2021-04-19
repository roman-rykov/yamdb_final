from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrAuthenticated,
    IsModeratorOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCUDSerializer,
    TitleSerializer,
)


def get_title(view):
    return get_object_or_404(Title, id=view.kwargs.get('title_id'))


def get_review(view):
    review = get_object_or_404(
        Review,
        id=view.kwargs.get('review_id'),
        title_id=view.kwargs.get('title_id'),
    )
    return review


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class ReviewModelViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrReadOnly | IsAuthorOrAuthenticated]

    def get_queryset(self):
        title = get_title(self)
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title_id=get_title(self))


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsModeratorOrReadOnly | IsAuthorOrAuthenticated]

    def get_queryset(self):
        review = get_review(self)
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review_id=get_review(self))


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.prefetch_related(
        'genre', 'category',
    ).annotate(rating=Avg('reviews__score')).all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return TitleCUDSerializer
        return TitleSerializer
