import os
import django
from db_connections import club_collection, matches_collection
from datetime import datetime
from core.models import Club, Match

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fanconnect.settings')
django.setup()

# Import clubs
for club in club_collection.find():
    club_obj, created = Club.objects.get_or_create(
        mongo_id=str(club['_id']),
        defaults={
            'name': club['name'],
            'founded': club['founded'],
            'stadium': club['stadium'],
            'location': {
                'city': club['location']['city'],
                'country': club['location']['country']
            },
            'players': [
                {'name': player['name'], 'position': player['position']}
                for player in club['players']
            ],
        }
    )

# Import matches
for match in matches_collection.find():
    home_team = Club.objects.get(mongo_id=str(match['home_team_id']))
    away_team = Club.objects.get(mongo_id=str(match['away_team_id']))
    match_date = datetime.strptime(match['date'], "%Y-%m-%d %H:%M:%S")
    # match_date = timezone.make_aware(match['date'], timezone.get_current_timezone())

    Match.objects.get_or_create(
        home_team=home_team,
        away_team=away_team,
        mongo_id=str(match['_id']),
        defaults={
            'competition': match['competition'],
            'venue': match['venue'],
            'city': match['city'],
            'country': match['country'],
            'date': match_date,
            'status': match['status'],
            'attendance': match['attendance'],
            'referee': match['referee'],
            'season': match['season'],
            'win_team': Club.objects.get(mongo_id=str(match.get('win_team_id'))) if match.get('win_team_id') else None,
        }
    )
