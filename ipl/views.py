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
import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .serializers import MatchSerializer, DeliverySerializer

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

# @cache_page(CACHE_TTL)
def matches_won(request):
    winner_season = Match.objects.all().values('season', 'winner').order_by('season').distinct()
    queryset = Match.objects.exclude(winner=None).values(
        'winner', 'season').annotate(count=Count('winner')).order_by('season')
    seasons_list = sorted(list(set([row['season'] for row in winner_season])))
    winners = list(set([row['winner'] for row in winner_season]))
    data = transform_data(queryset, seasons_list, winners)
    return JsonResponse(data)

def transform_data(queryset, seasons_list, winners):
    team_with_data = {}
    for team in winners:
        team_with_data[team] = [0]*len(seasons_list)
    for row in queryset:
        season = row['season']
        winner = row['winner']
        count = row['count']
        team_with_data[winner][seasons_list.index(season)] = count
    team_data = [{'name': data, 'data': team_with_data[data]} for data in team_with_data]
    return {'season': seasons_list, 'team_data': team_data}

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
    delivery = Delivery.objects.get(pk=id)
    form = DeliveryForm(instance=delivery)
    return render(request, 'get_match.html', {'form':form})

@csrf_exempt
def create_match(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    match = Match(**body)
    match.save()
    return JsonResponse({"result": "OK"})

@csrf_exempt
def create_delivery(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    delivery = Delivery(**body)
    delivery.save()
    return JsonResponse({"result": "OK"})
    

@csrf_exempt
def get_delivery_api(request,id):
    if request.method == 'DELETE':
        delivery = Delivery.objects.get(pk=id).delete()
        delivery = {'result':"deleted"}
    elif request.method == 'GET':
        try:
            delivery = Delivery.objects.values().get(pk=id)
        except Delivery.DoesNotExist:
            raise Http404
    elif request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        Delivery.objects.filter(pk=id).update(**body)
        delivery = {'result': 'updated'}
    return JsonResponse(delivery, safe=False)

@csrf_exempt
def get_match_api(request,id):
    if request.method == 'DELETE':
        match = Match.objects.get(pk=id).delete()
        match = {'result':"deleted"}
    elif request.method == 'GET':
        try:
            match = Match.objects.values().get(pk=id)
        except Match.DoesNotExist:
            raise Http404
    elif request.method == 'PUT':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        Match.objects.filter(pk=id).update(**body)
        match = {'result': 'updated'}

    return JsonResponse(match, safe=False)


class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides a get method handler.
    """
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_match = self.queryset.get(pk=kwargs["pk"])
            return Response(MatchSerializer(a_match).data)
        except Match.DoesNotExist:
            return Response(
                data={
                    "message": "Match with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class DeliveryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides a get method handler.
    """
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def get(self, request, *args, **kwargs):
        try:
            a_delivery = self.queryset.get(pk=kwargs["pk"])
            return Response(DeliverySerializer(a_delivery).data)
        except Delivery.DoesNotExist:
            return Response(
                data={
                    "message": "Delivery with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class CreateMatchView(generics.CreateAPIView):
    serializer_class = MatchSerializer

class CreateDeliveryView(generics.CreateAPIView):
    serializer_class = DeliverySerializer