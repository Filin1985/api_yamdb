from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import (
    User,
    Category,
    Review,
    Comment,
    Title,
    Genre,
    GenreTitle
)


class Command(BaseCommand):
    """Загрузка данных, для тестирования."""
    help = 'Загрузка данных'

    def handle(self, *args, **options):
        users = []
        for row in DictReader(open('./static/data/users.csv')):
            users.append(User(**row))
        User.objects.bulk_create(users, 50)

        categories = []
        for row in DictReader(open('./static/data/category.csv')):
            categories.append(**row)
        Category.objects.bulk_create(categories, 50)

        titles = []
        for row in DictReader(open('./static/data/titles.csv')):
            titles.append(**row)
        Title.objects.bulk_create(titles, 50)

        reviews = []
        for row in DictReader(open('./static/data/review.csv')):
            reviews.append(**row)
        Review.objects.bulk_create(reviews, 50)

        comments = []
        for row in DictReader(open('./static/data/comments.csv')):
            comments.append(**row)
        Comment.objects.bulk_create(comments, 50)

        genres = []
        for row in DictReader(open('./static/data/genre.csv')):
            genres.append(**row)
        Genre.objects.bulk_create(genres, 50)

        genres_titles = []
        for row in DictReader(open('./static/data/genre_title.csv')):
            genres_titles.append(**row)
        GenreTitle.objects.bulk_create(genres_titles, 50)
