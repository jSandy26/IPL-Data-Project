from django.shortcuts import render

# Create your views here.
from ipl.models import Match, Delivery
from django.forms import ModelForm
from django.db.models import Count, Sum, Case, When, F, FloatField
from django.db.models.functions import Cast
from django.http import JsonResponse, Http404
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def index(request):
    return render(request, 'index.html', context={})


@cache_page(CACHE_TTL)
def matches_per_season(request):
    num_matches_season = Match.objects.all().values('season').annotate(count = Count('season')).order_by('season')
    context = {}
    for season in num_matches_season:
        context[season['season']] = season['count']
    seasons = list(context.keys())
    matches = list(context.values())
    return JsonResponse({'seasons': seasons, 'matches': matches})

@cache_page(CACHE_TTL)
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

@cache_page(CACHE_TTL)
def extra_runs(request):
    queryset = Delivery.objects.filter(match_id__season = 2016, is_super_over=False).values('bowling_team').annotate(sum=Sum('extra_runs')).order_by('sum')
    extra_runs_per_team = {}

    for team in queryset:
        extra_runs_per_team[team['bowling_team']] = team['sum']
    teams = list(extra_runs_per_team.keys())
    extra_runs_conceded = list(extra_runs_per_team.values())
    return JsonResponse({'teams': teams, 'extra_runs': extra_runs_conceded})

@cache_page(CACHE_TTL)
def economy_bowlers(request):
    queryset = Delivery.objects.filter(match_id__season = 2015, is_super_over=False).values('bowler').annotate(runs=(Sum('total_runs') - (Sum('legbye_runs') + Sum('bye_runs')))).annotate(balls= Count('ball') - Count(Case(When(noball_runs__gt=0, then=0))) - Count(Case(When(wide_runs__gt=0, then=0)))).annotate(economy= Cast((F('runs')/(F('balls')/6.0)), FloatField())).order_by('economy')[:10]

    bowlers = []
    economies = []
    for bowler in queryset:
        bowlers.append(bowler['bowler'])
        economies.append(bowler['economy'])
    return JsonResponse({'bowlers':bowlers, 'economies':economies})

@cache_page(CACHE_TTL)
def economies_at_death(request):
    queryset = Delivery.objects.filter(over__gt=15, is_super_over=False).values('bowler').annotate(runs=(Sum('total_runs') - (Sum('legbye_runs') + Sum('bye_runs')))).annotate(balls= Count('ball') - Count(Case(When(noball_runs__gt=0, then=0))) - Count(Case(When(wide_runs__gt=0, then=0)))).annotate(economy= Cast((F('runs')/(F('balls')/6.0)), FloatField())).order_by('economy')
    bowlers = []
    economies = []
    for bowler in queryset:
        if bowler['balls'] > 24 and bowler['economy'] < 8:
            bowlers.append(bowler['bowler'])
            economies.append(bowler['economy'])
    return JsonResponse({'bowlers':bowlers, 'economies':economies})

@cache_page(CACHE_TTL)
def economical_teams_at_death(request):
    queryset = Delivery.objects.filter(over__gt=15, is_super_over=False).values('bowling_team').annotate(runs=(Sum('total_runs'))).annotate(balls= Count('ball') - Count(Case(When(noball_runs__gt=0, then=0))) - Count(Case(When(wide_runs__gt=0, then=0)))).annotate(economy= Cast((F('runs')/(F('balls')/6.0)), FloatField())).order_by('economy')
    teams = []
    economies = []
    for team in queryset:
        teams.append(team['bowling_team'])
        economies.append(team['economy'])
    return JsonResponse({'teams':teams, 'economies':economies})


class MatchForm(ModelForm):
   class Meta:
       model = Match
       fields = '__all__'

class DeliveryForm(ModelForm):
   class Meta:
       model = Delivery
       fields = '__all__'

def get_match(request, id):
   match = Match.objects.get(pk=id)
   form = MatchForm(instance=match)
   return render(request,'get_match.html',{'form':form})


def get_delivery(request, id):
    id += 300922
    delivery = Delivery.objects.get(pk=id)
    form = DeliveryForm(instance=delivery)
    return render(request, 'get_match.html', {'form':form})

@csrf_exempt
def create_match(request):
  body_unicode = request.body.decode('utf-8')
  print('un',body_unicode)
  body = json.loads(body_unicode)
  print('body',body)
  u = Matches(**body)
  print('u',u)
  u.save()
  return JsonResponse({"result": "OK"})

def create_delivery(request):
    form = DeliveryForm()
    return render(request, 'create_form.html', {'form': form})

def get_delivery_api(request,id):
    id += 300922
    if request.method == 'DELETE':
        delivery = Delivery.objects.get(pk=id).delete()
        delivery = {'result':"deleted"}
    elif request.method == 'GET':
        try:
            delivery = Delivery.objects.values().get(pk=id)
        except Delivery.DoesNotExist:
            raise Http404
    return JsonResponse(delivery, safe=False)

def get_match_api(request,id):
    if request.method == 'DELETE':
        match = Match.objects.get(pk=id).delete()
        match = {'result':"deleted"}
    elif request.method == 'GET':
        try:
            match = Match.objects.values().get(pk=id)
        except Match.DoesNotExist:
            raise Http404
    return JsonResponse(match, safe=False)