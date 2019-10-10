from django.shortcuts import render

# Create your views here.
from ipl.models import Match, Delivery
from django.db.models import Count, Sum, Case, When, F, FloatField
from django.db.models.functions import Cast
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html', context={})

def matches_per_season(request):
    num_matches_season = Match.objects.all().values('season').annotate(count = Count('season')).order_by('season')
    context = {}
    for season in num_matches_season:
        context[season['season']] = season['count']
    seasons = list(context.keys())
    matches = list(context.values())
    return JsonResponse({'seasons': seasons, 'matches': matches})


def matches_won(request):
    seasons = Match.objects.all().values('season').order_by('season').distinct()
    teams = Match.objects.exclude(winner=None).values('winner').order_by('winner').distinct()
    queryset = Match.objects.exclude(winner=None).values('winner','season').annotate(count=Count('winner')).order_by('season')
    seasons_list = []
    for season in seasons:
        seasons_list.append(season['season'])
    team_wins_per_season = {}
    for team in teams:
        team_wins_per_season[team['winner']] = [0]*len(seasons)
    for row in queryset:
        season = row['season']
        winner = row['winner']
        count = row['count']
        team_wins_per_season[winner][seasons_list.index(season)] = count
    team_data = []
    for data in team_wins_per_season:
        team_data.append({'name': data, 'data': team_wins_per_season[data]})
    return JsonResponse({'season': seasons_list, 'team_data' : team_data})

def extra_runs(request):
    queryset = Delivery.objects.filter(match_id__season = 2016, is_super_over=False).values('bowling_team').annotate(sum=Sum('extra_runs')).order_by('sum')
    extra_runs_per_team = {}

    for team in queryset:
        extra_runs_per_team[team['bowling_team']] = team['sum']
    teams = list(extra_runs_per_team.keys())
    extra_runs_conceded = list(extra_runs_per_team.values())
    return JsonResponse({'teams': teams, 'extra_runs': extra_runs_conceded})

def economy_bowlers(request):
    queryset = Delivery.objects.filter(match_id__season = 2015, is_super_over=False).values('bowler').annotate(runs=(Sum('total_runs') - (Sum('legbye_runs') + Sum('bye_runs')))).annotate(balls= Count('ball') - Count(Case(When(noball_runs__gt=0, then=0))) - Count(Case(When(wide_runs__gt=0, then=0)))).annotate(economy= Cast((F('runs')/(F('balls')/6.0)), FloatField())).order_by('economy')[:10]

    bowlers = []
    economies = []
    for bowler in queryset:
        bowlers.append(bowler['bowler'])
        economies.append(bowler['economy'])
    return JsonResponse({'bowlers':bowlers, 'economies':economies})


   