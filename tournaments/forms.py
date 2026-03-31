from django import forms
from .models import Tournament

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            "name",
            "discipline",
            "description",
            "start_time",
            "location",
            "application_deadline",
            "max_teams",
            "max_participants",
            "is_active",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "application_deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["max_teams"].required = False
        self.fields["max_participants"].required = False

    def clean(self):
        cleaned_data = super().clean()
        discipline = cleaned_data.get("discipline")
        max_teams = cleaned_data.get("max_teams")
        max_participants = cleaned_data.get("max_participants")

        if discipline == "SOCCER":
            if not max_teams:
                self.add_error("max_teams", "Max teams is required for soccer tournaments.")
            elif discipline in ["CHESS", "TENNIS"]:
                if not max_participants:
                    self.add_error("max_participants", "Max participants is required for individual tournaments.")
            return cleaned_data