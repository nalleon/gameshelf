import json
import os
import random
from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from faker.providers import lorem

from classifications.models import Platform
from games.models import Game

fake = Faker()
fake.add_provider(lorem)

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate social fixtures for users, collections, libraries, wishlists, reviews and favorites.'

    FIXTURE_FILES = {
        'users': 'users.json',
        'profiles': 'profiles.json',
        'libraries': 'libraries.json',
        'library_items': 'library_items.json',
        'collections': 'collections.json',
        'collection_items': 'collection_items.json',
        'wishlists': 'wishlists.json',
        'wishlist_items': 'wishlist_items.json',
        'reviews': 'reviews.json',
        'media': 'review_media.json',
        'favorites': 'favorites.json',
    }

    COLORS = ['#79A998', '#5E81AC', '#BF616A', '#A3BE8C', '#EBCB8B', '#D08770', '#B48EAD']

    COLLECTION_NAMES = [
        'Favorites', 'Completed Games', 'Retro Collection', 'Multiplayer',
        'JRPG Masterpieces', 'Indie Gems', 'Backlog',
        'Physical Games', 'Digital Collection',
    ]

    LIBRARY_STATUSES = ['CMP', 'PLY', 'PSD', 'DRP', 'PLN']
    ITEM_TYPES = ['P', 'D']

    REVIEW_SENTENCES = [
        'One of the best games I have ever played.',
        'Amazing gameplay and soundtrack.',
        'Could not stop playing.',
        'A bit repetitive but still fun.',
        'Masterpiece.',
        'Overrated but enjoyable.',
        'Fantastic atmosphere.',
        'Combat system is incredible.',
        'Story was disappointing.',
        'Loved every second of it.',
    ]

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=25)

    # ---------------- MAIN ----------------

    def handle(self, *args, **options):

        print('DB:', settings.DATABASES)
        print('Games count:', Game.objects.count())
        print('Platforms count:', Platform.objects.count())

        self.fixtures = {k: [] for k in self.FIXTURE_FILES.keys()}

        self.games = list(Game.objects.values('id'))
        self.platforms = list(Platform.objects.values('id'))

        self.review_pk = 1
        self.media_pk = 1
        self.favorite_pk = 1

        if not self.games:
            self.stdout.write(self.style.ERROR('No games found'))
            return

        if not self.platforms:
            self.stdout.write(self.style.ERROR('No platforms found'))
            return

        self.generate_users(options['users'])
        self.generate_collections()
        self.generate_wishlists()
        self.generate_reviews()
        self.generate_favorites()

        output_dir = os.path.join(settings.BASE_DIR, 'fixtures')
        os.makedirs(output_dir, exist_ok=True)

        for key, filename in self.FIXTURE_FILES.items():
            self.write_fixture(os.path.join(output_dir, filename), self.fixtures[key])

        self.stdout.write(self.style.SUCCESS('Social fixtures generated'))

    # ---------------- USERS ----------------

    def generate_users(self, total):
        for i in range(1, total + 1):
            user_pk = i

            self.fixtures['users'].append({
                'model': 'auth.user',
                'pk': user_pk,
                'fields': {
                    'username': fake.unique.user_name(),
                    'email': fake.unique.email(),
                    'password': 'pbkdf2_sha256$600000$fake$fakehash',
                    'is_active': True,
                    'is_staff': False,
                    'is_superuser': False,
                    'date_joined': timezone.now().isoformat(),
                },
            })

            self.fixtures['profiles'].append({
                'model': 'users.profile',
                'pk': user_pk,
                'fields': {
                    'user': user_pk,
                    'bio': fake.text(max_nb_chars=120),
                    'verified': random.choice([True, False, False]),
                    'role': 'U',
                    'avatar': 'avatars/default.png',
                },
            })

            self.fixtures['libraries'].append({
                'model': 'libraries.library',
                'pk': user_pk,
                'fields': {
                    'user': user_pk,
                    'is_private': random.choice([True, False]),
                    'created_at': timezone.now().isoformat(),
                    'updated_at': timezone.now().isoformat(),
                },
            })

            self.generate_library_items(user_pk)

    # ---------------- LIBRARY ITEMS ----------------

    def generate_library_items(self, library_pk):

        selected_games = random.sample(self.games, min(len(self.games), random.randint(5, 20)))
        used = set()

        for game in selected_games:
            for _ in range(2):
                platform_id = random.choice(self.platforms)['id']
                key = (library_pk, game['id'], platform_id)

                if key in used:
                    continue

                used.add(key)

                self.fixtures['library_items'].append({
                    'model': 'libraries.libraryitem',
                    'fields': {
                        'library': library_pk,
                        'game': game['id'],
                        'platform': platform_id,
                        'status': random.choice(self.LIBRARY_STATUSES),
                        'is_private': random.choice([True, False]),
                        'hours_played': round(random.uniform(1, 400), 1),
                        'created_at': timezone.now().isoformat(),
                        'updated_at': timezone.now().isoformat(),
                    },
                })

    # ---------------- COLLECTIONS ----------------

    def generate_collections(self):
        for user_id in range(1, len(self.fixtures['users']) + 1):

            total = random.randint(1, 4)
            used_names = set()

            for i in range(total):

                available = [n for n in self.COLLECTION_NAMES if n not in used_names]
                if not available:
                    break

                name = random.choice(available)
                used_names.add(name)

                collection_pk = user_id * 100 + i

                self.fixtures['collections'].append({
                    'model': 'game_collections.collection',
                    'pk': collection_pk,
                    'fields': {
                        'user': user_id,
                        'name': name,
                        'is_private': random.choice([True, False]),
                        'created_at': timezone.now().isoformat(),
                    },
                })

                self.generate_collection_items(collection_pk)

    def generate_collection_items(self, collection_pk):

        selected_games = random.sample(self.games, random.randint(3, 15))
        used = set()

        for game in selected_games:
            key = (game['id'],)

            if key in used:
                continue

            used.add(key)

            self.fixtures['collection_items'].append({
                'model': 'game_collections.collectionitem',
                'fields': {
                    'collection': collection_pk,
                    'game': game['id'],
                    'platform': random.choice(self.platforms)['id'],
                    'type': random.choice(self.ITEM_TYPES),
                    'is_private': random.choice([True, False]),
                    'created_at': timezone.now().isoformat(),
                },
            })

    # ---------------- WISHLISTS ----------------

    def generate_wishlists(self):
        for user_id in range(1, len(self.fixtures['users']) + 1):

            self.fixtures['wishlists'].append({
                'model': 'game_collections.wishlist',
                'pk': user_id,
                'fields': {
                    'user': user_id,
                    'name': 'My Wishlist',
                    'is_private': random.choice([True, False]),
                    'created_at': timezone.now().isoformat(),
                },
            })

            self.generate_wishlist_items(user_id)

    def generate_wishlist_items(self, wishlist_pk):

        selected_games = random.sample(self.games, random.randint(5, 15))

        for game in selected_games:

            self.fixtures['wishlist_items'].append({
                'model': 'game_collections.wishlistitem',
                'fields': {
                    'wishlist': wishlist_pk,
                    'game': game['id'],
                    'platform': random.choice(self.platforms)['id'],
                    'type': random.choice(self.ITEM_TYPES),
                    'priority': random.randint(1, 10),
                    'annotation': random.choice(['', 'Must play', 'Waiting for sale']),
                    'is_private': random.choice([True, False]),
                    'created_at': timezone.now().isoformat(),
                },
            })
            
    # ---------------- REVIEWS ----------------
    def generate_reviews(self):
        for user_id in range(1, len(self.fixtures['users']) + 1):

            selected_games = random.sample(self.games, random.randint(2, 10))

            for game in selected_games:

                review_pk = self.review_pk

                self.fixtures['reviews'].append({
                    'model': 'games.review',
                    'pk': review_pk,
                    'fields': {
                        'content': random.choice(self.REVIEW_SENTENCES) + ' ' + fake.text(200),
                        'recommend': random.choice([True, True, False]),
                        'game': game['id'],
                        'author': user_id,
                        'created_at': timezone.now().isoformat(),
                        'updated_at': timezone.now().isoformat(),
                    },
                })

                # ---------------- MEDIA (OPCIONAL POR REVIEW) ----------------
                if random.random() < 0.6:

                    media_count = random.randint(1, 3)

                    for _ in range(media_count):

                        self.fixtures['media'].append({
                            'model': 'games.media',
                            'pk': self.media_pk,
                            'fields': {
                                'image': self.generate_fake_image(review_pk),
                                'review': review_pk,
                            },
                        })

                        self.media_pk += 1

                self.review_pk += 1
    # ---------------- FAVORITES ----------------

    def generate_favorites(self):

        order = 1

        for user_id in range(1, len(self.fixtures['users']) + 1):

            selected_games = random.sample(self.games, random.randint(3, 10))
            used = set()

            for game in selected_games:

                key = (game['id'],)
                if key in used:
                    continue

                used.add(key)

                self.fixtures['favorites'].append({
                    'model': 'games.favoriteitem',
                    'pk': self.favorite_pk,
                    'fields': {
                        'game': game['id'],
                        'platform': random.choice(self.platforms)['id'],
                        'user': user_id,
                        'order': order,
                    },
                })

                self.favorite_pk += 1
                order += 1

    # ---------------- HELPERS ----------------

    def write_fixture(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    def generate_fake_image(self, review_id):
        media_dir = os.path.join(settings.BASE_DIR, 'fixtures', 'media')
        os.makedirs(media_dir, exist_ok=True)

        color = tuple(random.randint(0, 255) for _ in range(3))

        size = (
            random.randint(400, 1200),
            random.randint(300, 900)
        )

        filename = f'review_{review_id}_{self.media_pk}.png'
        path = os.path.join(media_dir, filename)

        img = Image.new('RGB', size, color)
        img.save(path)

        return f'media/{filename}'