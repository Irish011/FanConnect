from functools import wraps
from django.shortcuts import render
from bson.objectid import ObjectId
from db_connections import user_collection, matches_collection, club_collection, predictions_collections


def fetch_user_document(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            user_document = user_collection.find_one({"username": request.user.username})
            if not user_document:
                return render(request, 'core/matches.html', {
                    'upcoming_matches': [],
                    'completed_matches': [],
                })
            request.user_document = user_document
        return func(request, *args, **kwargs)

    return wrapper


def fetch_favorite_clubs(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user_document'):
            return func(request, *args, **kwargs)

        favorite_club_ids = request.user_document.get('favorite_clubs', [])
        favorite_clubs = []
        for club_id in favorite_club_ids:
            club = club_collection.find_one({'_id': ObjectId(club_id)})
            if club:
                favorite_clubs.append(club)
        request.favorite_clubs = favorite_clubs
        # print(favorite_clubs)
        return func(request, *args, **kwargs)

    return wrapper


def fetch_matches(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'favorite_clubs'):
            return func(request, *args, **kwargs)

        favorite_club_ids = [club['_id'] for club in request.favorite_clubs]
        upcoming_matches = list(matches_collection.find({
            '$and': [
                {'$or': [
                    {'home_team_id': {'$in': favorite_club_ids}},
                    {'away_team_id': {'$in': favorite_club_ids}}
                ]},
                {'status': 'Upcoming'}
            ]
        }))

        completed_matches = list(matches_collection.find({
            '$and': [
                {'$or': [
                    {'home_team_id': {'$in': favorite_club_ids}},
                    {'away_team_id': {'$in': favorite_club_ids}}
                ]},
                {'status': 'Completed'}
            ]
        }))
        for match in upcoming_matches + completed_matches:
            match['home_team_name'] = get_club_name(match['home_team_id'])
            match['away_team_name'] = get_club_name(match['away_team_id'])
            match['match_id'] = str(match['_id'])

        request.upcoming_matches = upcoming_matches
        request.completed_matches = completed_matches

        return func(request, *args, **kwargs)

    return wrapper


def check_predictions(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'upcoming_matches'):
            return func(request, *args, **kwargs)

        match_ids = [str(match['_id']) for match in request.upcoming_matches]
        user_id = request.user_document['_id']
        predicted = list(predictions_collections.find(
            {'user_id': ObjectId(user_id), 'match_id': {'$in': [ObjectId(id) for id in match_ids]}}
        ))

        predicted_match_ids = [str(p['match_id']) for p in predicted]
        for match in request.upcoming_matches:
            match['is_predicted'] = str(match['_id']) in predicted_match_ids

        return func(request, *args, **kwargs)

    return wrapper


def get_club_name(club_id):
    club = club_collection.find_one({"_id": ObjectId(club_id)})
    return club['name'] if club else "Unknown"
