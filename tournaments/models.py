from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
User=settings.AUTH_USER_MODEL

TEAM_SPORTS = ["SCOCCER"]
INDIVIDUAL_SPORTS = ["CHESS", "TENNIS"]

class Tournament(models.Model):
    DISCIPLINE_CHOICES = [
        ("CHESS", "Chess"),
        ("TENNIS", "Tennis"),
        ("SOCCER", "Soccer"),
    ]

    name=models.CharField(max_length=100)
    discipline=models.CharField(max_length=20, choices=DISCIPLINE_CHOICES)
    organizer=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='organized_tournaments',)
    description=models.TextField(blank=True)
    start_time=models.DateTimeField()
    location=models.CharField(max_length=200)
    max_participants=models.PositiveIntegerField(null=True, blank=True)
    max_teams=models.PositiveIntegerField(null=True, blank=True)
    application_deadline=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    @property
    def is_team_based(self):
        return self.discipline in TEAM_SPORTS

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_time and self.start_time<timezone.now():
           raise ValidationError("Tournament start time must be in the future.") 
        if self.start_time and self.application_deadline and self.application_deadline>=self.start_time:
           raise ValidationError("Application deadline must be before the start time.")    
        
    
class Match(models.Model):
    tournament=models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")
    team1=models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="match_team1", null=True, blank=True)
    team2=models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="match_team2", null=True, blank=True)
    winner_team=models.ForeignKey("teams.Team", null=True, blank=True, on_delete=models.SET_NULL, related_name="wins")
    
    participant1=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="match_participant1", null=True, blank=True)
    participant2=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="match_participant2", null=True, blank=True)
    winner_participant=models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="participant_wins")

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.tournament.is_team_based:
            return f"{self.team1} vs {self.team2}"
        return f"{self.participant1} vs {self.participant2}"
    

    