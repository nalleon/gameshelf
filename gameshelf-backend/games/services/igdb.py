import time
import requests
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings
from games.models import Game
from classifications.models import Genre, Platform, Developer, Publisher, Region, Edition




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

def get_defaults():
    region, _ = Region.objects.get_or_create(name='to_be_add', defaults={'acronym': 'TBA', 'igdb_id': 0})
    edition, _ = Edition.objects.get_or_create(name='Standard', defaults={'description': 'Default edition'})
    return region, edition

def sync_igdb_regions():
    '''
    Trae todas las regiones oficiales desde IGDB y las guarda en la base de datos,
    asignando también la organización de rating correspondiente.
    '''
    token = get_igdb_token()
    url = 'https://api.igdb.com/v4/release_date_regions'

    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    query = '''
    fields id, region;
    limit 500;
    '''

    response = requests.post(url, data=query, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    REGION_RATINGS = {
        1: 'PEGI',        # europe
        2: 'ESRB',        # north_america
        3: 'PEGI',        # australia
        4: 'PEGI',        # new_zealand
        5: 'CERO',        # japan
        6: 'GRAC',        # china
        7: 'GRAC',        # asia
        8: None,          # worldwide
        9: 'GRAC',        # korea
        10: 'GRAC',       # brazil
    }

    created_count = 0
    for region in data:
        igdb_id = region.get('id')
        name = region.get('region')
        if igdb_id is None or not name:
            continue

        rating_org = REGION_RATINGS.get(igdb_id)
        

        obj, created = Region.objects.update_or_create(
            igdb_id=igdb_id,
            defaults={
                'name': name,
                'rating_organization': rating_org
            }
        )
        if created:
            created_count += 1

    print(f'Regiones creadas o actualizadas: {created_count}')
    
def save_games_to_db(games_data, default_region, default_edition, token):
    RATING_CATEGORIES = {
        1: 'Three', 2: 'Seven', 3: '12', 4: '16', 5: '18', 6: 'Eighteen',
        8: 'E', 9: 'E10', 10: 'T', 11: 'M', 12: 'AO', 13: 'Mature',
        14: 'CERO_A', 15: 'CERO_B', 16: 'CERO_C', 17: 'CERO_D', 18: 'CERO_Z',
        20: 'USK_0', 21: 'USK_6', 22: 'USK_12', 23: 'USK_16', 24: 'USK_18', 25: 'USK_18+',
        28: 'GRAC_Eight', 29: 'GRAC_Twelve', 30: 'GRAC_Sixteen', 31: 'GRAC_Eighteen',
        32: 'CLASS_IND_18',
        33: 'ACB_R18', 34: 'ACB_Mature', 35: 'ACB_Restricted', 37: 'ACB_Adults',
    }

    mature_thresholds = {
        'PEGI': ['Eighteen'],
        'ESRB': ['M', 'AO'],
        'CERO': ['CERO_Z'],
        'USK': ['USK_18'],
        'GRAC': ['GRAC_Eighteen'],
        'CLASS_IND': ['CLASS_IND_18'],
        'ACB': ['ACB_R18'],
    }

    created_count = 0
    skipped_count = 0

    all_age_rating_ids = []
    for g in games_data:
        for rating in g.get('age_ratings', []):
            if 'id' in rating:
                all_age_rating_ids.append(str(rating['id']))

    all_age_rating_ids = list(set(all_age_rating_ids))
    age_ratings_map = fetch_age_ratings(all_age_rating_ids, token)
    print(age_ratings_map)

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

            game, created = Game.objects.get_or_create(
                title=title,
                released_at=released_at,
                edition=default_edition,
                region=region_obj,
                defaults={'description': (g.get('summary') or '')[:500]}
            )

            if created:
                created_count += 1
            else:
                skipped_count += 1

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
            region_org = region_obj.rating_organization
            print('ANTES DEL IF')
            print(region_org)
            print(g.get('age_ratings'))
            print(g)
            print(game)
            print('=======================================')
            if region_org and g.get('age_ratings'):
                print('HOLA')
                for rating in g['age_ratings']:
                    rating_id = str(rating.get('id'))
                    real_rating = age_ratings_map.get(int(rating_id))
                    if not real_rating:
                        continue

                    rating_org_id = real_rating.get('organization')
                    rating_value_id = real_rating.get('rating_category')
                    rating_value_str = RATING_CATEGORIES.get(rating_value_id)
                    if not rating_value_str:
                        continue

                    org_map = {1:'PEGI',2:'ESRB',3:'CERO',4:'USK',5:'GRAC',6:'CLASS_IND',7:'ACB'}
                    if org_map.get(rating_org_id) == region_org:
                        selected_rating = {'org': region_org, 'value': rating_value_str}
                        break

                            
                if selected_rating:
                    game.age_rating = selected_rating['value']
                    
                    mature_values = mature_thresholds.get(selected_rating['org'], [])
                    game.mature_content = selected_rating['value'] in mature_values
                else:
                    game.age_rating = 'TBA'
                    game.mature_content = True

                game.save(update_fields=['age_rating', 'mature_content'])
    return created_count, skipped_count

def fetch_age_ratings(age_rating_ids, token):
    '''
    Consulta IGDB /age_ratings para traer los valores reales.
    '''
    if not age_rating_ids:
        return {}

    url = 'https://api.igdb.com/v4/age_ratings'
    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    ids_str = ','.join(age_rating_ids)
    query = f'''
    fields id, rating, rating_category, category, organization;
    where id = ({ids_str});
    limit {len(age_rating_ids)};
    '''

    response = requests.post(url, data=query, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Devolvemos un dict id -> rating completo
    return {r['id']: r for r in data}

def fetch_all_release_dates(game_ids, token):
    all_release_dates = []
    offset = 0
    batch_size = 500

    headers = {
        'Client-ID': settings.IGDB_CLIENT_ID,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
    }

    while True:
        query_release_dates = f'''
        fields game, date, region, release_region, platform;
        where game = ({game_ids});
        limit {batch_size};
        offset {offset};
        '''

        response = requests.post('https://api.igdb.com/v4/release_dates', data=query_release_dates, headers=headers)
        response.raise_for_status()

        data = response.json()
        if not data:
            break

        all_release_dates.extend(data)
        offset += batch_size

    return all_release_dates

def import_games(request):
    token = get_igdb_token()
    default_region, default_edition = get_defaults()

    # sincronizar regiones antes de importar
    sync_igdb_regions()

    total_to_fetch = 50
    batch_size = 50
    total_created = 0
    total_skipped = 0

    for offset in range(0, total_to_fetch, batch_size):
        query = f'''
        fields 
            id,
            name,
            summary,
            first_release_date,
            genres.name,
            platforms.name,
            involved_companies.company.name,
            involved_companies.developer,
            involved_companies.publisher,
            age_ratings.rating,
            age_ratings.rating_category;
        where version_parent = null;
        limit {batch_size};
        offset {offset};
        '''

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
            


        created_count, skipped_count = save_games_to_db(games_data, default_region, default_edition, token)
        total_created += created_count
        total_skipped += skipped_count
        time.sleep(0.3)

    return JsonResponse({
        'created': total_created,
        'skipped': total_skipped,
        'total_requested': total_to_fetch,
    })