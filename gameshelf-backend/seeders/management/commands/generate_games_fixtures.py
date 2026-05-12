import json
import os
import time
from collections import defaultdict
from datetime import datetime

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Generate game fixtures from IGDB with regions and ratings'

    BASE_URL = 'https://api.igdb.com/v4'
    TIMEOUT = 30
    AGE_RATINGS_BATCH_SIZE = 200
    FIXTURE_FILES = {
        'games': 'games.json',
        'genres': 'genres.json',
        'platforms': 'platforms.json',
        'developers': 'developers.json',
        'publishers': 'publishers.json',
        'regions': 'regions.json',
    }

    RATING_CATEGORIES = {
        1: 'Three',
        2: 'Seven',
        3: '12',
        4: '16',
        5: '18',
        6: 'Eighteen',
        8: 'E',
        9: 'E10',
        10: 'T',
        11: 'M',
        12: 'AO',
        13: 'Mature',
        14: 'CERO_A',
        15: 'CERO_B',
        16: 'CERO_C',
        17: 'CERO_D',
        18: 'CERO_Z',
        20: 'USK_0',
        21: 'USK_6',
        22: 'USK_12',
        23: 'USK_16',
        24: 'USK_18',
        28: 'GRAC_Eight',
        29: 'GRAC_Twelve',
        30: 'GRAC_Sixteen',
        31: 'GRAC_Eighteen',
        32: 'CLASS_IND_18',
        33: 'ACB_R18',
        34: 'ACB_Mature',
        35: 'ACB_Restricted',
        37: 'ACB_Adults',
    }

    MATURE_THRESHOLDS = {
        'PEGI': ['Eighteen'],
        'ESRB': ['M', 'AO', 'Mature'],
        'CERO': ['CERO_Z'],
        'USK': ['USK_18'],
        'GRAC': ['GRAC_Eighteen'],
        'CLASS_IND': ['CLASS_IND_18'],
        'ACB': ['ACB_R18'],
        'IARC': ['+18'],
    }

    REGION_RATINGS = {
        1: 'PEGI',
        2: 'ESRB',
        3: 'PEGI',
        4: 'PEGI',
        5: 'CERO',
        6: 'GRAC',
        7: 'GRAC',
        8: 'IARC',
        9: 'GRAC',
        10: 'GRAC',
    }

    ORG_MAP = {
        1: 'PEGI',
        2: 'ESRB',
        3: 'CERO',
        4: 'USK',
        5: 'GRAC',
        6: 'CLASS_IND',
        7: 'ACB',
        8: 'IARC',
    }

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=500)

    def handle(self, *args, **options):
        self.token = self.get_igdb_token()

        self.headers = {
            'Client-ID': settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
        }

        self.now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        self.fixtures = {k: [] for k in self.FIXTURE_FILES.keys()}

        self.processed_genre_ids = set()
        self.processed_platform_ids = set()
        self.processed_developer_ids = set()
        self.processed_publisher_ids = set()
        self.slug_counter = defaultdict(int)
        self.used_slugs = set()
        self.seen_games = set()

        self.parent_games = {}

        output_dir = os.path.join(settings.BASE_DIR, 'fixtures')
        os.makedirs(output_dir, exist_ok=True)

        self.sync_regions()

        games = self.fetch_games(max_games=options['limit'])

        age_rating_ids = self.collect_age_rating_ids(games)
        age_ratings_map = self.fetch_age_ratings(age_rating_ids)

        for g in games:
            self.process_game(g, age_ratings_map)

        for key, filename in self.FIXTURE_FILES.items():
            self.write_fixture(os.path.join(output_dir, filename), self.fixtures[key])

        self.stdout.write(self.style.SUCCESS('Done'))

    # -----------------------
    # IGDB
    # -----------------------

    def get_igdb_token(self):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': settings.IGDB_CLIENT_ID,
            'client_secret': settings.IGDB_CLIENT_SECRET,
            'grant_type': 'client_credentials',
        }
        res = requests.post(url, params=params, timeout=self.TIMEOUT)
        res.raise_for_status()
        return res.json()['access_token']

    def fetch_games(self, batch_size=500, max_games=10000):
        offset = 0
        all_games = []

        while len(all_games) < max_games:
            query = f"""
                fields id,name,summary,first_release_date,
                cover.image_id,
                genres.id,genres.name,
                platforms.id,platforms.name,
                involved_companies.developer,
                involved_companies.publisher,
                involved_companies.company.id,
                involved_companies.company.name,
                age_ratings.id,
                release_dates.date,
                release_dates.release_region;

                where game_type = 0 & first_release_date != null;

                limit {batch_size};
                offset {offset};
            """

            res = requests.post(
                f'{self.BASE_URL}/games',
                headers=self.headers,
                data=query.encode('utf-8'),
                timeout=self.TIMEOUT,
            )

            if res.status_code != 200:
                self.stdout.write(res.text)
                res.raise_for_status()

            data = res.json()
            if not data:
                break

            all_games.extend(data)
            offset += batch_size

            self.stdout.write(f'Fetched {len(all_games)} games...')
            time.sleep(0.6)

        return all_games[:max_games]

    # -----------------------
    # AGE RATINGS
    # -----------------------

    def collect_age_rating_ids(self, games):
        return list({r['id'] for g in games for r in g.get('age_ratings', []) if r.get('id')})


    def fetch_age_ratings(self, ids):
        if not ids:
            return {}

        ratings_map = {}

        for i in range(0, len(ids), self.AGE_RATINGS_BATCH_SIZE):
            batch_ids = ids[i : i + self.AGE_RATINGS_BATCH_SIZE]

            query = f"""
                fields id,rating,rating_category,organization;
                where id = ({','.join(map(str, batch_ids))});
            """

            try:
                res = requests.post(
                    f'{self.BASE_URL}/age_ratings',
                    headers=self.headers,
                    data=query,
                    timeout=self.TIMEOUT,
                )

                if res.status_code != 200:
                    self.stdout.write(
                        self.style.WARNING(f'Error fetching age ratings batch {i}: {res.status_code}')
                    )
                    self.stdout.write(res.text)
                    continue

                data = res.json()

                for rating in data:
                    ratings_map[rating['id']] = rating

                self.stdout.write(
                    f'Fetched age ratings: {min(i + self.AGE_RATINGS_BATCH_SIZE, len(ids))}/{len(ids)}'
                )

                time.sleep(0.3)

            except requests.exceptions.Timeout:
                self.stdout.write(
                    self.style.WARNING(f'Timeout fetching age ratings batch starting at {i}')
                )

            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.WARNING(f'Error fetching age ratings batch starting at {i}: {e}')
                )

        return ratings_map
    # -----------------------
    # PROCESS GAME
    # -----------------------

    def process_game(self, g, age_ratings_map):
        genre_ids = self.get_or_create_genres(g.get('genres', []))
        platform_ids = self.get_or_create_platforms(g.get('platforms', []))
        dev_ids, pub_ids = self.get_or_create_companies(g.get('involved_companies', []))

        image_id = g.get('cover', {}).get('image_id')

        base_game_id = g['id']

        for rd in g.get('release_dates', []):
            ts = rd.get('date')
            if not ts:
                continue

            released_at = datetime.utcfromtimestamp(ts).date()
            release_region_id = rd.get('release_region')

            # -------------------------
            # AGE RATING
            # -------------------------
            rating_value = 'TBA'
            mature = True

            region_org = self.REGION_RATINGS.get(release_region_id)

            selected = None
            fallback = None

            for r in g.get('age_ratings', []):
                real = age_ratings_map.get(r['id'])
                if not real:
                    continue

                org = self.ORG_MAP.get(real.get('organization'))
                label = self.RATING_CATEGORIES.get(real.get('rating_category'))

                if not label:
                    continue

                if region_org and org == region_org:
                    selected = (org, label)
                    break

                if not fallback:
                    fallback = (org, label)

            final = selected or fallback

            if final:
                org, label = final
                rating_value = label
                mature = label in self.MATURE_THRESHOLDS.get(org, [])

            pk = int(f'{g["id"]}{release_region_id or 0}')

            # -------------------------
            # PARENT GAME LOGIC
            # -------------------------
            if base_game_id not in self.parent_games:
                self.parent_games[base_game_id] = pk
                parent_pk = None
            else:
                parent_pk = self.parent_games[base_game_id]

            normalized_title = g['name'].strip().lower()

            slug = self.unique_slug(g['name'])

            key = (
                normalized_title,
                released_at.isoformat(),
                release_region_id or 0,
            )

            if key in self.seen_games:
                continue

            self.seen_games.add(key)

            self.fixtures['games'].append(
                {
                    'model': 'games.game',
                    'fields': {
                        'igdb_id': pk,
                        'title': g['name'],
                        'slug': slug,
                        'description': (g.get('summary') or '')[:500],
                        'released_at': released_at.isoformat(),
                        'region': release_region_id,
                        'parent_game_igdb': parent_pk,
                        'age_rating': rating_value,
                        'mature_content': mature,
                        'cover_default': self.build_cover_url(image_id),
                        'cover_detail': self.build_cover_url(image_id, 'original'),
                        'genres': genre_ids,
                        'platforms': platform_ids,
                        'developers': dev_ids,
                        'publishers': pub_ids,
                    },
                }
            )

    # -----------------------
    # HELPERS
    # -----------------------

    def write_fixture(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_or_create_genres(self, genres):
        ids = []

        for g in genres:
            if not g.get('id') or not g.get('name'):
                continue

            if g['id'] not in self.processed_genre_ids:
                self.fixtures['genres'].append(
                    {
                        'model': 'classifications.genre',
                        'pk': g['id'],
                        'fields': {'name': g['name'], 'slug': self.unique_slug(g['name'])},
                    }
                )
                self.processed_genre_ids.add(g['id'])

            ids.append(g['id'])

        return ids

    def get_or_create_platforms(self, platforms):
        ids = []

        for p in platforms:
            if not p.get('id') or not p.get('name'):
                continue

            if p['id'] not in self.processed_platform_ids:
                self.fixtures['platforms'].append(
                    {
                        'model': 'classifications.platform',
                        'pk': p['id'],
                        'fields': {'name': p['name'], 'slug': self.unique_slug(p['name'])},
                    }
                )
                self.processed_platform_ids.add(p['id'])

            ids.append(p['id'])

        return ids

    def get_or_create_companies(self, companies):
        dev_ids = []
        pub_ids = []

        for comp in companies:
            company = comp.get('company')
            if not company:
                continue

            cid = company.get('id')
            name = company.get('name')

            if not cid or not name:
                continue

            # DEVELOPERS
            if comp.get('developer'):
                if cid not in self.processed_developer_ids:
                    self.fixtures['developers'].append(
                        {
                            'model': 'classifications.developer',
                            'pk': cid,
                            'fields': {'name': name, 'slug': self.unique_slug(name)},
                        }
                    )
                    self.processed_developer_ids.add(cid)

                dev_ids.append(cid)

            # PUBLISHERS
            if comp.get('publisher'):
                if cid not in self.processed_publisher_ids:
                    self.fixtures['publishers'].append(
                        {
                            'model': 'classifications.publisher',
                            'pk': cid,
                            'fields': {'name': name, 'slug': self.unique_slug(name)},
                        }
                    )
                    self.processed_publisher_ids.add(cid)

                pub_ids.append(cid)

        return dev_ids, pub_ids

    def sync_regions(self):
        query = 'fields id,region; limit 200;'
        res = requests.post(
            f'{self.BASE_URL}/release_date_regions',
            headers=self.headers,
            data=query,
            timeout=self.TIMEOUT,
        )
        res.raise_for_status()

        for r in res.json():
            self.fixtures['regions'].append(
                {
                    'model': 'classifications.region',
                    'pk': r['id'],
                    'fields': {
                        'name': str(r['region']),
                        'slug': slugify(str(r['region'])),
                        'acronym': str(r['region'])[:2].upper(),
                        'igdb_id': r['id'],
                    },
                }
            )

    def build_cover_url(self, image_id, size='cover_big'):
        if not image_id:
            return None
        return f'https://images.igdb.com/igdb/image/upload/t_{size}/{image_id}.jpg'

    def unique_slug(self, name):
        base = slugify(name)
        slug = base
        counter = 1

        while slug in self.used_slugs:
            slug = f'{base}-{counter}'
            counter += 1

        self.used_slugs.add(slug)
        return slug
