from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated,)

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet

from .models import Category, Titles, Genre, GenreTitle
from .serializer import (
CategorySerializer,
TitleSerializer,
GenreSerializer,
GenreTitleSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticated,
                          IsAuthenticatedOrReadOnly,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GenreTitleViewSet(viewsets.ModelViewSet):
    queryset = GenreTitle.objects.all()
    serializer_class = GenreTitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


