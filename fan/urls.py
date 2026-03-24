from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('schedule/', views.schedule, name='schedule'),

    # User Preferences
    path('user_preference/create/', views.user_preference_create, name='user_preference_create'),
    path('user_preference/list/', views.user_preference_list, name='user_preference_list'),
    path('user_preference/update/<int:pk>/', views.user_preference_update, name='user_preference_update'),
    path('user_preference/delete/<int:pk>/', views.user_preference_delete, name='user_preference_delete'),
    path('preferences/', views.user_preference_list, name='preferences'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('set-theme/', views.set_theme, name='set_theme'),

    # Ajax
    path('get_leagues/', views.get_leagues, name='get_leagues'),
    path('get_teams/', views.get_teams, name='get_teams'),

    # Export
    path('export/', views.export, name='export'),

    # League reports
    path('report/leagues/', views.league_report_view, name='league_report_view'),  # страница со списком лиг
    path('report/league/<int:league_id>/', views.download_league_report, name='report_league_single'),

     path('report/users/', views.download_user_report, name='download_user_report'),
]
