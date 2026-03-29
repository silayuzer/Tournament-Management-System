from django.db import models
from django.conf import settings
from tournaments.models import Tournament
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    created_by= models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    captain = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='captained_teams', null=True, blank=True)

    class Meta:
        unique_together = ('name', 'tournament')

    def clean(self):
        if self.tournament.teams.count() >= self.tournament.max_teams:
            raise ValidationError("This tournament is already full.")
    
    def __str__(self):
        return self.name