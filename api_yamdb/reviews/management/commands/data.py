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
        for row in DictReader(open('./static/data/users.csv')):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=['first_name'],
                last_name=['last_name']
            )
            user.save()

        for row in DictReader(open('./static/data/category.csv')):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            category.save()

        for row in DictReader(open('./static/data/titles.csv')):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']),
            )
            title.save()

        for row in DictReader(open('./static/data/review.csv')):
            print(row)
            review = Review(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=int(row['author'])),
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        for row in DictReader(open('./static/data/comments.csv')):
            comment = Comment(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date'],
            )
            comment.save()

        for row in DictReader(open('./static/data/genre.csv')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        for row in DictReader(open('./static/data/genre_title.csv')):
            genre_title = GenreTitle(
                id=row['id'],
                title=Title.objects.get(id=row['title_id']),
                genre=Genre.objects.get(id=row['genre_id']),
            )
            genre_title.save()
