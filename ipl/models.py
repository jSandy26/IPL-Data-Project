from django.db import models
from postgres_copy import CopyManager


# Create your models here.

class Match(models.Model):
   season = models.PositiveIntegerField()
   city = models.CharField(max_length=200, null=True)
   date = models.DateField()
   team1 = models.CharField(max_length=100, null=True)
   team2 = models.CharField(max_length=100, null=True)
   toss_winner = models.CharField(max_length=100, null=True)
   toss_decision = models.CharField(max_length=100, null=True)
   result = models.CharField(max_length=100, null=True)
   dl_applied = models.PositiveIntegerField(null=True)
   winner = models.CharField(max_length=100, null=True)
   win_by_runs = models.PositiveIntegerField(null=True)
   win_by_wickets = models.PositiveIntegerField(null=True)
   player_of_match = models.CharField(max_length=100, null=True)
   venue = models.CharField(max_length=200, null=True)
   umpire1 = models.CharField(max_length=100, null=True)
   umpire2 = models.CharField(max_length=100, null=True)
   umpire3 = models.CharField(max_length=100, null=True)
   objects = CopyManager()


class Delivery(models.Model):
   match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
   inning = models.PositiveIntegerField()
   batting_team = models.CharField(max_length=100)
   bowling_team = models.CharField(max_length=100)
   over = models.PositiveIntegerField()
   ball = models.PositiveIntegerField()
   batsman = models.CharField(max_length=100, null=True)
   non_striker = models.CharField(max_length=100, null=True)
   bowler = models.CharField(max_length=100, null=True)
   is_super_over = models.PositiveIntegerField()
   wide_runs = models.PositiveIntegerField()
   bye_runs = models.PositiveIntegerField()
   legbye_runs = models.PositiveIntegerField()
   noball_runs = models.PositiveIntegerField()
   penalty_runs = models.PositiveIntegerField()
   batsman_runs = models.PositiveIntegerField()
   extra_runs = models.PositiveIntegerField()
   total_runs = models.PositiveIntegerField()
   player_dismissed = models.CharField(max_length=50, null=True)
   dismissal_kind = models.CharField(max_length=50, null=True)
   fielder = models.CharField(max_length=50, null=True)
   objects = CopyManager()