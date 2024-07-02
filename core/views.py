from django.shortcuts import render, get_object_or_404, redirect
from .decorators import fetch_user_document, fetch_favorite_clubs, check_predictions, fetch_matches, get_club_name
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UsersForm
from django.http import HttpResponse
from db_connections import user_collection, matches_collection, club_collection, predictions_collections
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from bson.objectid import ObjectId


def index(request):
    if request.user.is_authenticated:
        user_data = user_collection.find_one({'username': request.user.username})
        if user_data:
            favorite_club_ids = user_data.get('favorite_clubs', [])
            favorite_clubs = []
            for club_id in favorite_club_ids:
                club = club_collection.find_one({'_id': ObjectId(club_id)})
                if club:
                    favorite_clubs.append(club['name'])
            return render(request, 'core/index.html', {'favorite_clubs': favorite_clubs})
    return render(request, 'core/index.html')


def get_all_club(request):
    clubs = list(club_collection.find())
    return render(request, 'core/clubs.html', {'clubs': clubs})


def get_match_id(matches):
    return [str(match['_id']) for match in matches]


def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            age = form.cleaned_data['age']
            email = form.cleaned_data['email']
            mobile_number = form.cleaned_data['mobile_number']
            country = form.cleaned_data['country']
            password = make_password(form.cleaned_data['password'])
            favorite_clubs = form.cleaned_data['favorite_clubs']
            favorite_club_ids = [ObjectId(club_id) for club_id in favorite_clubs]
            user_collection.insert_one({
                'username': username,
                'age': age,
                'email': email,
                'mobile_number': mobile_number,
                'country': country,
                'password': password,
                'favorite_clubs': favorite_club_ids,
                'rewards': 0,
            })
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'core/register_user.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def profile(request):
    user_document = user_collection.find_one({'username': request.user.username})
    favorite_club_ids = user_document.get('favorite_clubs', [])
    favorite_club_object_ids = [ObjectId(club_id) for club_id in favorite_club_ids]
    favorite_clubs = list(club_collection.find({'_id': {'$in': favorite_club_object_ids}}))
    user_document['favorite_clubs_names'] = [club['name'] for club in favorite_clubs]
    return render(request, 'core/profile.html', {
        'user_document': user_document,
    })


@fetch_user_document
@fetch_favorite_clubs
@fetch_matches
@check_predictions
def matches_view(request):
    if not request.user.is_authenticated:
        completed_matches = list(matches_collection.find({"status": "Completed"}))
        upcoming_matches = list(matches_collection.find({"status": "Upcoming"}))

        for match in upcoming_matches + completed_matches:
            match['home_team_name'] = get_club_name(match['home_team_id'])
            match['away_team_name'] = get_club_name(match['away_team_id'])

        return render(request, 'core/matches.html', {
            'upcoming_matches': upcoming_matches,
            'completed_matches': completed_matches,
        })
    return render(request, 'core/matches.html', {
        'upcoming_matches': request.upcoming_matches,
        'completed_matches': request.completed_matches,
    })


@login_required
@fetch_user_document
@fetch_favorite_clubs
@fetch_matches
@check_predictions
def predict(request):
    if request.method == 'POST':
        prediction = request.POST.get('prediction')
        return redirect('matches')

    return render(request, 'core/predict.html', {
        'upcoming_matches': request.upcoming_matches,
        'match_ids': get_match_id(request.upcoming_matches),
        "user_id": request.user_document['_id'],
    })


@login_required
@fetch_user_document
@fetch_favorite_clubs
def edit_clubs(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            selected_club_ids = form.cleaned_data['favorite_clubs']
            user_document = request.user_document
            user_collection.update_one({'_id': user_document['_id']},
                                       {'$set': {'favorite_clubs': selected_club_ids}})
            return redirect('profile')
    else:
        form = UsersForm(initial={'favorite_clubs': [str(club['_id']) for club in request.favorite_clubs]})

    return render(request, 'core/edit_clubs.html', {
        'form': form,
    })


@login_required
@fetch_user_document
@fetch_favorite_clubs
@fetch_matches
@check_predictions
def match_poll(request, match_id):
    try:
        match = next((match for match in request.upcoming_matches if str(match['_id']) == match_id), None)
    except:
        match = None

    if not match:
        return HttpResponse("Match not found", status=404)

    if request.method == 'POST':
        win_team_id = request.POST.get('prediction')
        user_document = request.user_document
        user_id = user_document['_id']
        predictions_collections.insert_one({
            'user_id': user_id,
            'match_id': ObjectId(match_id),
            'win_team_id': ObjectId(win_team_id)
        })
        return redirect('match_details')

    return render(request, 'core/match_predict.html', {'match': match})

# def admin_home(request):
#     return render(request, 'core/admin_home.html')
#
#
# def index(request):
#     if request.user.is_authenticated:
#         user_data = user_collection.find_one({'username': request.user.username})
#         if user_data:
#             favorite_club_ids = user_data.get('favorite_clubs', [])
#
#             favorite_clubs = []
#             for club_id in favorite_club_ids:
#                 club = club_collection.find_one({'_id': ObjectId(club_id)})
#                 if club:
#                     favorite_clubs.append(club['name'])
#
#             return render(request, 'core/index.html', {'favorite_clubs': favorite_clubs})
#     return render(request, 'core/index.html')
#
#
# def get_club_name(club_id):
#     club = club_collection.find_one({"_id": ObjectId(club_id)})
#     return club['name'] if club else "Unknown"
#
#
# def get_all_club(request):
#     clubs = list(club_collection.find())
#     return render(request, 'core/clubs.html', {'clubs': clubs})
#
#
# def home(request):
#     teams = Team.objects.all()
#     return render(request, 'core/home.html', {'teams': teams})
#
#
# def team_detail(request, team_id):
#     team = get_object_or_404(Team, id=team_id)
#     posts = team.posts.all()
#     return render(request, 'core/team_detail.html', {'teams': team,
#                                                      'posts': posts})
#
#
# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     return render(request, 'core/post_detail.html', {'post', post})
#
#
# def register_team(request):
#     if request.method == 'POST':
#         form = TeamForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = TeamForm()
#     return render(request, 'core/register_team.html', {'form': form})
#
#
# def register_user(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             age = form.cleaned_data['age']
#             email = form.cleaned_data['email']
#             mobile_number = form.cleaned_data['mobile_number']
#             country = form.cleaned_data['country']
#             password = make_password(form.cleaned_data['password'])
#             favorite_clubs = form.cleaned_data['favorite_clubs']
#             favorite_club_ids = [ObjectId(club_id) for club_id in favorite_clubs]
#             # favorite_clubs = [ObjectId(club_id) for club_id in form.cleaned_data['favorite_clubs']]
#
#             user_collection.insert_one({
#                 'username': username,
#                 'age': age,
#                 'email': email,
#                 'mobile_number': mobile_number,
#                 'country': country,
#                 'password': password,
#                 'favorite_clubs': favorite_club_ids,
#                 'rewards': 0,
#             })
#
#             return redirect('home')
#     else:
#         form = UserForm()
#
#     return render(request, 'core/register_user.html', {'form': form})
#
#
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form.add_error(None, "Invalid username or password")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'registration/login.html', {'form': form})
#
#
# @login_required
# def profile(request):
#     user = request.user
#     # Assuming you have a MongoDB connection
#     # client = MongoClient('mongodb://localhost:27017/')
#     # db = client['FanConnect']
#     # users_collection = db['users']
#     # clubs_collection = db['clubs']
#     user_document = user_collection.find_one({'username': user.username})
#     favorite_club_ids = user_document.get('favorite_clubs', [])
#     favorite_club_object_ids = [ObjectId(club_id) for club_id in favorite_club_ids]
#     favorite_clubs = list(club_collection.find({'_id': {'$in': favorite_club_object_ids}}))
#     user_document['favorite_clubs_names'] = [club['name'] for club in favorite_clubs]
#     # user_document = users_collection.find_one({'username': user.username})
#     return render(request, 'core/profile.html', {
#         'user_document': user_document,
#     })
#
#
# def get_match_to(match):
#     return {
#         "home_team_name": match["home_team_name"],
#         "match_id": match["_id"],
#         "away_team_name": match["away_team_name"],
#         "date": match["date"],
#     }
#
#
# # def matches_view(request):
# #     favorite_clubs = request.user.profile.favorite_clubs  # Assuming favorite clubs are stored in the user profile
# #
# #     upcoming_matches = Match.objects.filter(
# #         (Q(home_team_id__in=favorite_clubs) | Q(away_team_id__in=favorite_clubs)) & Q(status='Upcoming')
# #     )
# #
# #     completed_matches = Match.objects.filter(
# #         (Q(home_team_id__in=favorite_clubs) | Q(away_team_id__in=favorite_clubs)) & Q(status='Completed')
# #     )
# #
# #     context = {
# #         'upcoming_matches': upcoming_matches,
# #         'completed_matches': completed_matches,
# #     }
# #     return render(request, 'core/matches.html', context)
#
# def get_match_id(matches):
#     return [str(match['_id']) for match in matches]
#
#
# def matches_view(request):
#     user = request.user
#     if not user.is_authenticated:
#         completed_matches = list(matches_collection.find({"status": "Completed"}))
#         upcoming_matches = list(matches_collection.find({"status": "Upcoming"}))
#
#         for match in upcoming_matches + completed_matches:
#             match['home_team_name'] = get_club_name(match['home_team_id'])
#             match['away_team_name'] = get_club_name(match['away_team_id'])
#
#         return render(request, 'core/matches.html', {
#             'upcoming_matches': upcoming_matches,
#             'completed_matches': completed_matches,
#         })
#
#     user_document = user_collection.find_one({"username": request.user.username})
#     if not user_document:
#         return render(request, 'core/matches.html', {
#             'upcoming_matches': [],
#             'completed_matches': [],
#         })
#     favorite_clubs = user_document['favorite_clubs']
#
#     upcoming_matches = list(matches_collection.find({
#         '$and': [
#             {'$or': [
#                 {'home_team_id': {'$in': favorite_clubs}},
#                 # [ObjectId('667d90d311f62f86c25c7eae')
#                 {'away_team_id': {'$in': favorite_clubs}}
#             ]},
#             {'status': 'Upcoming'}
#         ]
#     }))
#
#     completed_matches = matches_collection.find({
#         '$and': [
#             {'$or': [
#                 {'home_team_id': {'$in': favorite_clubs}},
#                 {'away_team_id': {'$in': favorite_clubs}}
#             ]},
#             {'status': 'Completed'}
#         ]
#     })
#     upcoming_matches_tos = []
#     completed_matches_tos = []
#
#     for match in upcoming_matches:
#         match['home_team_name'] = get_club_name(match['home_team_id'])
#         match['away_team_name'] = get_club_name(match['away_team_id'])
#         match['match_id'] = str(match['_id'])
#         # upcoming_matches_tos.append(get_match_to(match))
#
#     for match in completed_matches:
#         match['home_team_name'] = get_club_name(match['home_team_id'])
#         match['away_team_name'] = get_club_name(match['away_team_id'])
#         match['match_id'] = str(match['_id'])
#         completed_matches_tos.append(get_match_to(match))
#
#     match_ids = [str(match['_id']) for match in upcoming_matches]
#     user_id = user_document['_id']
#     predicted = list(predictions_collections.find(
#         {'user_id': ObjectId(user_id), 'match_id': {'$in': [ObjectId(id) for id in match_ids]}}
#     ))
#
#     predicted_match_ids = [str(p['match_id']) for p in predicted]
#     for match in upcoming_matches:
#         match['is_predicted'] = str(match['_id']) in predicted_match_ids
#
#     return render(request, 'core/matches.html', {
#         'upcoming_matches': upcoming_matches,
#         'completed_matches': completed_matches_tos,
#         'match_id': match_ids,
#     })
#
#
# def get_user_id(users):
#     return [str(user['_id']) for user in users]
#
#
# @login_required
# def predict(request):
#     upcoming_matches = list(matches_collection.find({"status": "Upcoming"}))
#     for match in upcoming_matches:
#         match['home_team_name'] = get_club_name(match['home_team_id'])
#         match['away_team_name'] = get_club_name(match['away_team_id'])
#         match['match_id'] = str(match['_id'])
#         # match['is_predicted'] = match.get('is_predicted')
#
#         # print(match['is_predicted'])
#
#     match_ids = get_match_id(upcoming_matches)
#     user_document = user_collection.find_one({"username": request.user.username})
#     user_id = user_document['_id']
#     predicted = list(predictions_collections.find(
#         {'user_id': ObjectId(user_id), 'match_id': {'$in': [ObjectId(id) for id in match_ids]}}))
#
#     predict = [str(p['match_id']) for p in predicted]
#     for match in upcoming_matches:
#         match['is_predicted'] = match['match_id'] in predict
#     # predicted = predictions_collections.find_one({"user_id": user_id, "match_id": match_ids})
#     # print(match_ids)
#     if request.method == 'POST':
#         prediction = request.POST.get('prediction')
#
#         return redirect('matches')
#
#     return render(request, 'core/predict.html',
#                   {'upcoming_matches': upcoming_matches, 'match_ids': match_ids, "user_id": user_id})
#
#
# @login_required
# def edit_clubs(request):
#     user_document = user_collection.find_one({"username": request.user.username})
#
#     if request.method == 'POST':
#         form = UsersForm(request.POST)
#         if form.is_valid():
#             favorite_clubs = form.cleaned_data['favorite_clubs']
#             user_collection.update_one(
#                 {'_id': user_document['_id']},
#                 {'$set': {'favorite_clubs': [ObjectId(club) for club in favorite_clubs]}}
#             )
#             return redirect('profile')
#     else:
#         initial_favorite_clubs = [str(club) for club in user_document.get('favorite_clubs', [])]
#         form = UsersForm(initial={'favorite_clubs': initial_favorite_clubs})
#
#     return render(request, 'core/edit_clubs.html', {'form': form})
#
#
# @login_required
# def match_poll(request, match_id):
#     try:
#         match = matches_collection.find_one({"_id": ObjectId(match_id)})
#     except:
#         match = None
#
#     if not match:
#         return render(request, 'core/match_predict.html', {'error': 'Match not found'})
#
#     match['home_team_name'] = get_club_name(match['home_team_id'])
#     match['away_team_name'] = get_club_name(match['away_team_id'])
#
#     if request.method == 'POST':
#         win_team_id = request.POST.get('prediction')
#         # Fetch the user document to get the correct MongoDB ObjectId
#         user_document = user_collection.find_one({"username": request.user.username})
#         if user_document:
#             user_id = user_document['_id']
#             prediction_data = {
#                 'user_id': user_id,
#                 'match_id': ObjectId(match_id),
#                 'win_team_id': ObjectId(win_team_id)
#             }
#             # print(prediction_data)
#
#             predictions_collections.insert_one({
#                 'user_id': user_id,
#                 'match_id': ObjectId(match_id),
#                 'win_team_id': ObjectId(win_team_id)
#             })
#
#             # matches_collection.update_one(
#             #     {'_id': ObjectId(match_id)},
#             #     {'$set': {'is_predicted': True}}
#             # )
#
#             return redirect('match_details')
#
#     return render(request, 'core/match_predict.html', {'match': match})
