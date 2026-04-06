import time
import requests
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings
from games.models import Game, AgeRating
from classifications.models import Genre, Platform, Developer, Publisher, Region, Edition

IGDB_REGION_MAP = {
    1: 'USA',
    2: 'Europe',
    3: 'Japan',
    4: 'Australia',
    5: 'New Zealand',
    6: 'Global',
    7: 'Brazil',
    8: 'Mexico',
    9: 'Argentina',
    10: 'Germany',
}

REGION_TO_AGE_RATING = {
    'Global': 'pegi',
    'Europe': 'pegi',
    'USA': 'esrb',
    'Japan': 'cero',
    'Germany': 'usk',
    'Brazil': 'grb',
    'Argentina': 'class_ind',
}

def get_igdb_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": settings.IGDB_CLIENT_ID,
        "client_secret": settings.IGDB_CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

def get_defaults():
    region, _ = Region.objects.get_or_create(name="Global", defaults={"acronym": "GB"})
    edition, _ = Edition.objects.get_or_create(name="Standard", defaults={"description": "Default edition"})
    return region, edition

def save_games_to_db(games_data, default_region, default_edition):
    created_count = 0
    skipped_count = 0

    for g in games_data:
        title = g.get("name")
        if not title:
            skipped_count += 1
            continue

        timestamp = g.get("first_release_date")
        released_at = datetime.utcfromtimestamp(timestamp).date() if timestamp else datetime.today().date()

       
        for release in g.get("release_dates") or []:
            region_id = release.get("region")
            release_timestamp = release.get("date")
            
            if not release_timestamp:
                continue  # Saltamos si no hay fecha específica

            released_at = datetime.utcfromtimestamp(release_timestamp).date()
            region_name = IGDB_REGION_MAP.get(region_id, default_region.name)
            region_obj, _ = Region.objects.get_or_create(name=region_name)

            # Crear o recuperar el juego
            game, created = Game.objects.get_or_create(
                title=title,
                released_at=released_at,
                edition=default_edition,
                region=region_obj,
                defaults={'description': (g.get("summary") or "")[:500]}
            )

            if created:
                created_count += 1
            else:
                skipped_count += 1  # No se crea, pero actualizamos relaciones

            # Asociar géneros
            for genre in g.get("genres", []):
                if "name" in genre:
                    obj, _ = Genre.objects.get_or_create(name=genre["name"])
                    game.genres.add(obj)

            # Asociar plataformas
            for platform in g.get("platforms", []):
                if "name" in platform:
                    obj, _ = Platform.objects.get_or_create(name=platform["name"])
                    game.platforms.add(obj)

            # Developers y publishers
            for comp in g.get("involved_companies", []):
                company_data = comp.get("company")
                if not company_data:
                    continue
                company_name = company_data.get("name")
                if not company_name:
                    continue

                if comp.get("developer"):
                    dev, _ = Developer.objects.get_or_create(name=company_name)
                    game.developers.add(dev)

                if comp.get("publisher"):
                    pub, _ = Publisher.objects.get_or_create(name=company_name)
                    game.publishers.add(pub)

            # AgeRatings según IGDB
            for rating in g.get("age_ratings", []):
                rating_value = rating.get("rating")
                rating_region_id = rating.get("region")
                rating_region_name = IGDB_REGION_MAP.get(rating_region_id, region_name)
                rating_type = REGION_TO_AGE_RATING.get(rating_region_name, 'pegi')

                if rating_value is not None:
                    AgeRating.objects.get_or_create(
                        game=game,
                        age_rating=rating_type,
                        defaults={"rating": rating_value},
                    )

    return created_count, skipped_count


def import_games(request):
    token = get_igdb_token()
    default_region, default_edition = get_defaults()
    url = "https://api.igdb.com/v4/games"

    total_to_fetch = 500
    batch_size = 100

    total_created = 0
    total_skipped = 0

    for offset in range(0, total_to_fetch, batch_size):
        query = f"""
            fields name, summary, first_release_date,
                genres.name,
                platforms.name,
                involved_companies.company.name,
                involved_companies.developer,
                involved_companies.publisher,
                release_dates.date,
                release_dates.region,
                age_ratings.rating, age_ratings.rating_category;
            limit {batch_size};
            offset {offset};
            where version_parent = null;
            """

        headers = {
            "Client-ID": settings.IGDB_CLIENT_ID,
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        response = requests.post(url, data=query, headers=headers)
        if response.status_code == 403:
            return JsonResponse({"error": "403 Forbidden: posible rate limit o token expirado"}, status=403)
        response.raise_for_status()

        games_data = response.json()
        if not games_data:
            break

        created_count, skipped_count = save_games_to_db(games_data, default_region, default_edition)
        total_created += created_count
        total_skipped += skipped_count

        time.sleep(0.3)

    return JsonResponse({
        "created": total_created,
        "skipped": total_skipped,
        "total_requested": total_to_fetch,
    })