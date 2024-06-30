from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('post/<post_id>/', views.post_detail, name='post_detail'),
    path('register_user/', views.register_user, name='register_user'),
    path('register-team/', views.register_team, name='register_team'),
    path('get_all/', views.get_all_club, name='get_all_club'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('matches/', views.matches_view, name='match_details'),
    path('predict/', views.predict, name='predict'),
    path('predict/<str:match_id>/', views.match_poll, name='poll'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]