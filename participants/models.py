from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from tournaments.models import Tournament
from django.utils import timezone

# Create your models here.
class Participant(models.Model):
    tournament=models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="participants")
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participations")
    registered_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tournament", "user")

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.tournament.max_participants and \
              self.tournament.participants.exclude(pk=self.pk).count()>=self.tournament.max_participants:
               raise ValidationError(f"This tournament is full. Max {self.tournament.max_participants} participants allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user} - {self.tournament}"