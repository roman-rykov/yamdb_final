from django.db import models

class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Имя категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Имя категории')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Заголовок')
    year = models.DateField(
        verbose_name='Дата создания',
        null=True,
        blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='относящиеся категории',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    title = models.ForeignKey(
        Titles,
        verbose_name='Заголовок',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Имя категории',
        on_delete=models.CASCADE
    )