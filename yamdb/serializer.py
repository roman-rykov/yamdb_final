from .models import Category, GenreTitle, Genre, Titles
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Genre

class TitleSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('__all__')
        model = Titles


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = GenreTitle
        validators =[
            UniqueTogetherValidator(
                queryset=GenreTitle.objects.all(),
                fields=('title',))]

