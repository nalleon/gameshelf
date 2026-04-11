import time
import requests
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings
from games.models import Game
from classifications.models import Genre, Platform, Developer, Publisher, Region, Edition
from .utils import Utils
from shared.decorators import require_fields, require_http_methods, require_json_body, require_role
from users.decorators import auth_required
from django.views.decorators.csrf import csrf_exempt
from users.models import Profile
from rest_framework.response import Response
from games.tasks import deliver_new_games_notification
from django.db.models.functions import ExtractYear, ExtractMonth
# Method to import a list of games from IGDB to database. 
@csrf_exempt
@require_http_methods('POST')
@require_json_body
@require_fields(
    'quantity'
)
@auth_required
@require_role(Profile.Role.ADMIN)
def import_games(request):
    token = get_igdb_token()
    default_region, default_edition = get_defaults()

    sync_igdb_regions()
    payload = request.json
    quantity = payload['quantity']
    
    batch_size = 50
    total_created = 0
    total_skipped = 0

    for offset in range(0, quantity, batch_size):
        query = f"""
        fields 
            id,
            name,
            summary,
            first_release_date,
            cover.image_id,
            genres.name,
            platforms.name,
            involved_companies.company.name,
            involved_companies.developer,
            involved_companies.publisher,
            age_ratings.rating,
            age_ratings.rating_category
            ;
                
        where version_parent = null;
        limit {batch_size};
        offset {offset};
        """

        headers = {
            'Client-ID': settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json',
        }

        response = requests.post('https://api.igdb.com/v4/games', data=query, headers=headers)
        if response.status_code == 403:
            return JsonResponse({'error': '403 Forbidden: posible rate limit o token expirado'}, status=403)
        response.raise_for_status()

        games_data = response.json()
        if not games_data:
            break

        game_ids = ','.join(str(g['id']) for g in games_data if 'id' in g)
        release_dates_data = fetch_all_release_dates(game_ids, token)

        release_dates_map = {}
        for rd in release_dates_data:
            game_id = rd['game']
            release_dates_map.setdefault(game_id, []).append(rd)

        for g in games_data:
            g['release_dates'] = release_dates_map.get(g['id'], [])
            


        created_count, skipped_count, created_games = save_games_to_db(games_data, default_region, default_edition, token)
        total_created += created_count
        total_skipped += skipped_count
        time.sleep(0.3)
        
        filtered_games = exclude_mature_content(created_games)

        deliver_new_games_notification.delay(
            request.build_absolute_uri(),
            filtered_games
        )
    
    return JsonResponse({
        'created': total_created,
        'skipped': total_skipped,
        'total_requested': quantity,
    })
    


@csrf_exempt
@require_http_methods('GET')
def search_games_by_title(request):
    title = request.GET.get('title')
    if not title:
        return Response({'error': 'Missing title parameter'}, status=400)

    url = 'https://api.igdb.com/v4/games'
    limit = 50

    token = get_igdb_token()  

    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-Type': 'text/plain',  
    }

    query = f"""
        search "{title}";
        fields id,name,summary,first_release_date,
        cover.image_id,
        genres.name,
        platforms.name,
        involved_companies.company.name,
        involved_companies.developer,
        involved_companies.publisher,
        age_ratings.rating,age_ratings.rating_category;
        limit {limit};
    """

    response = requests.post(url, headers=headers, data=query.strip())
    response.raise_for_status()

    games = response.json()

    words = title.lower().split()
    filtered_games = [
        game for game in games
        if all(word in game['name'].lower() for word in words)
    ]

    return Response(filtered_games)

######################################
# Auxiliar methods
######################################

# Method to get the IGDB token
def get_igdb_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': settings.IGDB_CLIENT_ID,
        'client_secret': settings.IGDB_CLIENT_SECRET,
        'grant_type': 'client_credentials',
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['access_token']

# Method to create and/or get the defaults region and edition
def get_defaults():
    region, _ = Region.objects.get_or_create(name='to_be_add', defaults={'acronym': 'TBA', 'igdb_id': 0})
    edition, _ = Edition.objects.get_or_create(name='Standard', defaults={'description': 'Default edition'})
    return region, edition

# Method to sync GameShelf's regions with IGDB ones
def sync_igdb_regions():

    token = get_igdb_token()
    url = 'https://api.igdb.com/v4/release_date_regions'

    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    query = """
    fields id, region;
    limit 50;
    """

    response = requests.post(url, data=query, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    for region in data:
        igdb_id = region.get('id')
        name = region.get('region')
        if igdb_id is None or not name:
            continue

        rating_org = Utils.REGION_RATINGS.get(igdb_id)
        
        obj, created = Region.objects.update_or_create(
            igdb_id=igdb_id,
            defaults={
                'name': name,
                'rating_organization': rating_org
            }
        )
        
# Method to save a game obtained from IGDB into the database    
def save_games_to_db(games_data, default_region, default_edition, token):
    created_count = 0
    skipped_count = 0

    created_games = []
    all_age_rating_ids = []
    for g in games_data:
        for rating in g.get('age_ratings', []):
            if 'id' in rating:
                all_age_rating_ids.append(str(rating['id']))

    all_age_rating_ids = list(set(all_age_rating_ids))
    age_ratings_map = fetch_age_ratings(all_age_rating_ids, token)

    for g in games_data:
        title = g.get('name')
        if not title:
            skipped_count += 1
            continue

    
        game_releases = g.get('release_dates') or [{'date': g.get('first_release_date'), 'release_region': None}]

        for release in game_releases:
            release_timestamp = release.get('date')
            if not release_timestamp:
                continue

            released_at = datetime.utcfromtimestamp(release_timestamp).date()

            release_region_id = release.get('release_region')
            if release_region_id:
                try:
                    region_obj = Region.objects.get(igdb_id=release_region_id)
                except Region.DoesNotExist:
                    region_obj = default_region
            else:
                region_obj = default_region

            exists = Game.objects.annotate(
                year=ExtractYear('released_at'),
                month=ExtractMonth('released_at')
            ).filter(
                title=title,
                region=region_obj,
                year=released_at.year,
                month=released_at.month,
            ).exists()

            if exists:
                skipped_count += 1
                continue

            game = Game.objects.create(
                title=title,
                released_at=released_at,
                edition=default_edition,
                region=region_obj,
                description=(g.get('summary') or '')[:500]
            )

            created = True

            if created:
                created_count += 1
            else:
                skipped_count += 1

            cover_data = g.get('cover_default')
            image_id = cover_data.get('image_id') if cover_data else None
            cover_url_default = build_cover_url(image_id)
            
            if cover_url_default:
                game.cover_default = cover_url_default
                
            cover_url_detail = build_cover_url(image_id, 'original')
            
            if cover_url_detail:
                game.cover_detail = cover_url_detail
                
            for genre in g.get('genres', []):
                if 'name' in genre:
                    obj, _ = Genre.objects.get_or_create(name=genre['name'])
                    game.genres.add(obj)

            for platform in g.get('platforms', []):
                if 'name' in platform:
                    obj, _ = Platform.objects.get_or_create(name=platform['name'])
                    game.platforms.add(obj)

            for comp in g.get('involved_companies', []):
                company_data = comp.get('company')
                if not company_data:
                    continue
                company_name = company_data.get('name')
                if not company_name:
                    continue

                if comp.get('developer'):
                    dev, _ = Developer.objects.get_or_create(name=company_name)
                    game.developers.add(dev)

                if comp.get('publisher'):
                    pub, _ = Publisher.objects.get_or_create(name=company_name)
                    game.publishers.add(pub)

            selected_rating = None
            region_org = Utils.REGION_RATINGS.get(release_region_id)
            if region_org and g.get('age_ratings'):
                for rating in g['age_ratings']:
                    rating_id = str(rating.get('id'))
                    real_rating = age_ratings_map.get(int(rating_id))
                    if not real_rating:
                        continue

                    rating_org_id = real_rating.get('organization')
                    rating_value_id = real_rating.get('rating_category')
                    rating_value_str = Utils.RATING_CATEGORIES.get(rating_value_id)
                    if not rating_value_str:
                        continue

                    org_map = {1:'PEGI',2:'ESRB',3:'CERO',4:'USK',5:'GRAC',6:'CLASS_IND',7:'ACB'}
                    if org_map.get(rating_org_id) == region_org:
                        selected_rating = {'org': region_org, 'value': rating_value_str}
                        break

                            
                if selected_rating:
                    game.age_rating = selected_rating['value']
                    
                    mature_values = Utils.MATURE_THRESHOLDS.get(selected_rating['org'], [])
                    game.mature_content = selected_rating['value'] in mature_values 
                else:
                    game.age_rating = 'TBA'
                    game.mature_content = True
                    
                game.save()
                created_games.append(game)
                
    return created_count, skipped_count, created_games

# Method to fetch all existings age_ratings from IGDB 
def fetch_age_ratings(age_rating_ids, token):
    if not age_rating_ids:
        return {}

    url = 'https://api.igdb.com/v4/age_ratings'
    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    ids_str = ','.join(age_rating_ids)
    query = f"""
    fields id, rating, rating_category, category, organization;
    where id = ({ids_str});
    limit {len(age_rating_ids)};
    """

    response = requests.post(url, data=query, headers=headers)
    response.raise_for_status()
    data = response.json()

    return {r['id']: r for r in data}

# Method to fetch all release dates from a list of game based on their id
def fetch_all_release_dates(game_ids, token):
    all_release_dates = []
    url = 'https://api.igdb.com/v4/release_dates'
    offset = 0
    batch_size = 500

    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    while True:
        query_release_dates = f"""
        fields game, date, region, release_region, platform;
        where game = ({game_ids});
        limit {batch_size};
        offset {offset};
        """

        response = requests.post(url=url, data=query_release_dates, headers=headers)
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        all_release_dates.extend(data)
        offset += batch_size

    return all_release_dates

# Function to build an game's cover url based on IGDB
def build_cover_url(image_id, size='1080p'):
    if not image_id:
        return None
    return f'https://images.igdb.com/igdb/image/upload/t_{size}/{image_id}.jpg'

# Function to exclude games with marked with mature content from a list
def exclude_mature_content(games, limit=8):
    filtered_games = []

    for game in games:
        if not getattr(game, "mature_content", False):
            filtered_games.append(game)

        if len(filtered_games) == limit:
            break

    return filtered_games