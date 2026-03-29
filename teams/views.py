from django.forms import ValidationError
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts import forms
from teams.models import Team
from tournaments.models import Tournament
from .forms import TeamForm

# Create your views here.
@login_required
def register_team(request, tournament_id):
    tournament=get_object_or_404(Tournament, id=tournament_id)

    if timezone.now() > tournament.application_deadline:
        messages.error(request, "The application deadline has passed.")
        return redirect("tournaments:tournament_detail", tournament_id )
    
    if tournament.teams.count() >= tournament.max_teams:
        messages.error(request, "The maximum number of teams for this tournament has been reached.")
        return redirect("tournaments:tournament_detail", tournament_id )
        

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.tournament = tournament
            team.captain = request.user
            team.created_by = request.user

            try:
                team.full_clean()
                team.save()
                messages.success(request, "Team registered successfully!")
                return redirect("tournaments:tournament_detail", tournament.id)

            except ValidationError as e:
                for msg in e.messages:
                    form.add_error(None, msg)
    else:
        form = TeamForm(request.POST or None)
        class Meta:
            model = Team
            fields = ['name']
    return render(request, "teams/register_team.html", {"form": form, "tournament": tournament})