from auctions.models import Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()

        categories = [
            {'name': 'Collectibles & Art', 'icon': 'palette'},
            {'name': 'Home & Garden', 'icon': 'house'},
            {'name': 'Sporting Goods', 'icon': 'baseball-bat-ball'},
            {'name': 'Electronics', 'icon': 'mobile-screen-button'},
            {'name': 'Auto Parts & Accessories', 'icon': 'car'},
            {'name': 'Toys & Hobbies', 'icon': 'puzzle-piece'},
            {'name': 'Fashion', 'icon': 'shirt'},
            {'name': 'Musical Instruments & Gear', 'icon': 'guitar'},
        ]

        for category in categories:
            url_name = category['name'].lower().replace(' &', '').replace(' ', '-')
            Category.objects.create(name=category['name'], icon=category['icon'], url_name=url_name)
