from django.core.management.base import BaseCommand
import csv
from api.models import Category, Title, Genre
from auth_user.models import User


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
            User.objects.create(id=int(line['id']),
                                username=line['username'],
                                email=line['email'],
                                role=line['role'],
                                first_name=line['first_name'],
                                last_name=line['last_name'])


class Command(BaseCommand):
    """
    Read a CSV file using csv.DictReader
    """

    def handle(self, *args, **options):
        objects = ('users', 'category', 'genre', 'titles',)
        for object in objects:
            path = f'data/{object}.csv'

            with open(path, "r") as file_object:
                fill_base(file_object, object)

            print(f'The database is full of {object}!')
