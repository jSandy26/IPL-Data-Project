from django.urls import path

from . import views

app_name = 'ipl'
urlpatterns = [
    path('index', views.index, name='index'),
    path('api/first', views.matches_per_season, name='matches_per_season'),
    path('api/second', views.matches_won, name='matches_won'),
    path('api/third', views.extra_runs, name='extra_runs'),
    path('api/fourth', views.economy_bowlers, name='economy_bowlers'),
]