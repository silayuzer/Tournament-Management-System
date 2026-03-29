from django import forms
from .models import Tournament

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            "name",
            "description",
            "start_time",
            "location",
            "max_teams",
            "is_active",
        ]