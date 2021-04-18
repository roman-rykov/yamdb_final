import csv

from django.core.management.base import BaseCommand

from api.models import Category, Comment, Genre, Review, Title, User


def fill_base(file_object, object):
    reader = csv.DictReader(file_object, delimiter=',')
    for line in reader:
        if object == 'category':
            Category.objects.create(
                id=line['id'], name=line['name'], slug=line['slug'])
        if object == 'titles':
            category = Category.objects.get(id=int(line['category']))
            Title.objects.create(
                name=line['name'], year=line['year'], category=category)
        if object == 'genre':
            Genre.objects.create(
                id=line['id'], name=line['name'], slug=line['slug'])
        if object == 'users':
            User.objects.create(
                id=int(line['id']),
                username=line['username'],
                email=line['email'],
                role=line['role'],
                first_name=line['first_name'],
                last_name=line['last_name'],
            )
        if object == 'genre_title':
            Title.objects.get(id=int(line['title_id'])).genre.add(
                int(line['genre_id']))
        if object == 'review':
            Review.objects.create(
                id=int(line['id']),
                title_id=Title.objects.get(id=int(line['title_id'])),
                text=line['text'],
                author=User.objects.get(id=int(line['author'])),
                score=int(line['score']),
                pub_date=line['pub_date'],
            )
        if object == 'comments':
            Comment.objects.create(
                id=int(line['id']),
                review_id=Review.objects.get(id=int(line['review_id'])),
                text=line['text'],
                author=User.objects.get(id=int(line['author'])),
                pub_date=line['pub_date'],
            )


class Command(BaseCommand):
    """
    Read a CSV file using csv.DictReader
    """

    def handle(self, *args, **options):
        objects = (
            'users', 'category', 'genre', 'titles', 'genre_title', 'review',
            'comments',
        )
        for object in objects:
            path = f'data/{object}.csv'

            with open(path, "r") as file_object:
                fill_base(file_object, object)

            print(f'The database is full of {object}!')
