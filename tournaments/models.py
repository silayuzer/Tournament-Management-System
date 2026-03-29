from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
User=settings.AUTH_USER_MODEL
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
    max_participants=models.PositiveIntegerField()
    max_teams=models.PositiveIntegerField(default=10)
    application_deadline=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    def clean(self):
        if self.start_time<timezone.now():
           raise ValueError("Tournament start time must be in the future.") 
        if self.application_deadline>=self.start_time:
           raise ValueError("Application deadline must be before the start time.")    
        
    def __str__(self):
        return self.name
    
class Match(models.Model):
    tournament=models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="matches")
    team1=models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="match_team1")
    team2=models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="match_team2")
    created_at=models.DateTimeField(auto_now_add=True)
    winner=models.ForeignKey("teams.Team", null=True, blank=True, on_delete=models.SET_NULL, related_name="wins")

    def __str__(self):
        return f"{self.team1} vs {self.team2}"