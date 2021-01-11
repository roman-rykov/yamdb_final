from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Title(models.Model):
    name = models.CharField(verbose_name='название', max_length=200)
    year = models.IntegerField(verbose_name='год')  # TODO: сделать ограничение
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'


class Genre(models.Model):
    name = models.CharField(verbose_name='название', max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='ID произведения',
    )
    genre_id = models.ForeignKey(
        to=Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='ID жанра',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title_id', 'genre_id'), name='unique constraint',
            ),
        ]


class Review(models.Model):
    title_id = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='ID произведения',
    )
    text = models.TextField(verbose_name='текст', max_length=2000)
    score = models.IntegerField(
        verbose_name='оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(verbose_name='дата', auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.pub_date}: {self.text[:50]}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title_id'), name='review already exists',
            ),
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментарий',
    )
    text = models.TextField(verbose_name='текст', max_length=500)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(verbose_name='дата', auto_now_add=True)

    def __str__(self):
        return f'{self.author} on {self.pub_date}: {self.text[:50]}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
