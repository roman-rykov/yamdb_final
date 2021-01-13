from rest_framework import serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title_id', 'author'),
        #         message='cannot add another review'
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
