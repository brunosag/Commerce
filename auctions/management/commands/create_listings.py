from auctions.models import Category, Listing, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Listing.objects.all().delete()

        listings = [
            {
                'title': 'Ibanez RG421-BBS Electric Guitar',
                'description': 'The Ibanez S series first appeared in 1987. Since then presented this series is versatile and functional. Famous for the light, ergonomic mahogany body, it can sound like Allen else pick up guitars. The new, ball-bearing zero-resistance tremolo system allows even the smallest movements of the tremolo lever to come to life.The best luthiers always demonstrate their skills with the S Prestige proof again. PRESTIGE stands for high quality individual parts.',
                'price': 499.99,
                'category': 'Musical Instruments & Gear',
                'image': 'https://i.ebayimg.com/images/g/IA0AAOSw4A1f0KEU/s-l500.jpg',
            },
            {
                'title': 'Apple MacBook Air 13.3" A2179 Laptop,',
                'description': "From video-editing to gaming, It's 3.5x faster than the previous generation, with eight-cores of power providing an incredible performance. And for whisper-quiet operation, the improved thermal efficiency means it doesn't even need a fan. At the heart of the MacBook Air is a solid state drive with 512 GB of storage space. So, there's plenty of room for your work projects, movies, photos and music. And it's twice as fast as the previous MacBook Air, so you can load up your important files at lightning-speed.",
                'price': 1119.99,
                'category': 'Electronics',
                'image': 'https://www.megaeletronicos.com:4420/img/new-1-2-7-4-3-9-127439-1680549579_1680549579.jpg',
            },
        ]

        try:
            demo_user = User.objects.get(username='brunosag')
        except User.DoesNotExist:
            demo_user = User.objects.create_user(
                username='brunosag', email='demo_user@example.com', password='password'
            )

        for listing in listings:
            new_listing = Listing.objects.create(
                user=demo_user,
                title=listing['title'],
                description=listing['description'],
                price=listing['price'],
                image=listing['image'],
            )
            new_listing.categories.set(Category.objects.filter(name=listing['category']))
