import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name='название', max_length=100,
                            db_index=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='название', max_length=100,
                            db_index=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='название', max_length=200,
                            db_index=True)
    year = models.IntegerField(
        verbose_name='год',
        blank=True,
        null=True,
        db_index=True,
        validators=[MaxValueValidator(datetime.date.today().year)],
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=2000,
        blank=True,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        to=Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанры',
    )

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    SCORE_MESSAGE = 'Score must be between 1 and 10'

    title_id = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
    )
    text = models.TextField(verbose_name='текст', max_length=2000)
    score = models.IntegerField(
        verbose_name='оценка',
        validators=[
            MinValueValidator(1, message=SCORE_MESSAGE),
            MaxValueValidator(10, message=SCORE_MESSAGE),
        ],
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(verbose_name='дата', auto_now_add=True)

    class Meta:
        ordering = ['title_id', 'pub_date']
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title_id'), name='review already exists',
            ),
        ]

    def __str__(self):
        return f'{self.author} on {self.pub_date}: {self.text[:50]}'


class Comment(models.Model):
    review_id = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв',
    )
    text = models.TextField(verbose_name='текст', max_length=500)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор',
    )
    pub_date = models.DateTimeField(verbose_name='дата', auto_now_add=True)

    class Meta:
        ordering = ['review_id', 'pub_date']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'{self.author} on {self.pub_date}: {self.text[:50]}'
