from django.urls import path

from . import views

app_name = 'ipl'
urlpatterns = [
    path('index', views.index, name='index'),
    path('api/first', views.matches_per_season, name='matches_per_season'),
    path('api/second', views.matches_won, name='matches_won'),
    path('api/third', views.extra_runs, name='extra_runs'),
    path('api/fourth', views.economy_bowlers, name='economy_bowlers'),
    path('api/fifth', views.economies_at_death, name='economies_at_death'),
    path('api/fifth/1', views.economical_teams_at_death, name='economical_teams_at_death'),
    path('api/get/match/<int:id>', views.get_match, name='get_match'),
    path('api/get/delivery/<int:id>', views.get_delivery, name='get_delivery'),
    # path('api/create/match', views.create_match, name='create_match'),
    # path('api/create/delivery', views.create_delivery, name='create_delivery'),
    path('api/deliveries/delivery/<int:id>', views.get_delivery_api, name='get_delivery_api'),
    path('api/matches/match/<int:id>', views.get_match_api, name='get_match_api'),
    path('api/match/', views.create_match, name='create_match'),
    path('api/delivery', views.create_delivery, name='create_delivery'),
]