import random
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Tournament, Match
from participants.models import Participant
from teams.models import Team
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .utils import generate_bracket
from django.db.models import Q
from .forms import TournamentForm
from django.contrib import messages

# Create your views here.
@login_required
def create_tournament(request):
    if request.user.role != "organizer":
        return HttpResponseForbidden("You are not authorized to create a tournament.")

    if request.method == "POST":
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.organizer = request.user
            tournament.save()
            return redirect("homepage")
    else:
        form = TournamentForm()
    return render(request, "tournaments/create_tournament.html", {"form": form})

def tournament_list(request):
    tournaments = Tournament.objects.filter(
        start_time__gt=timezone.now()
    ).order_by("start_time")
    paginator=Paginator(tournaments, 10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    return render(request, "tournaments/tournament_list.html", {"page_obj": page_obj},)

def homepage(request):
    query=request.GET.get("q","")
    tournaments=Tournament.objects.all().order_by("start_time")
    if query:
        tournaments=tournaments.filter(
            Q(name__icontains=query) 
        )

    paginator=Paginator(tournaments, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    return render(request, "tournaments/homepage.html", {"page_obj": page_obj, "query": query})

def tournament_detail(request, tournament_id):
    tournament=get_object_or_404(Tournament, id=tournament_id) 
    teams=tournament.teams.all() if tournament.is_team_based else None
    participants=tournament.participants.all() if not tournament.is_team_based else None
    matches=Match.objects.filter(tournament=tournament)

    return render(request, "tournaments/tournament_detail.html", {
        "tournament": tournament, 
        "teams": teams, 
        "participants": participants,
        "matches": matches
    })

@login_required
def register_participant(request, tournament_id):
    tournament=get_object_or_404(Tournament, id=tournament_id)

    if tournament.is_team_based:
        messages.error(request, "This tournament is team-based tournament.")
        return redirect("tournaments:tournament_detail", tournament_id)
    
    if timezone.now() > tournament.application_deadline:
        messages.error(request, "The application deadline for this tournament has passed.")
        return redirect("tournaments:tournament_detail", tournament_id)
    
    if tournament.max_participants and tournament.participants.count() >= tournament.max_participants:
        messages.error(request, "This tournament is full.")
        return redirect("tournaments:tournament_detail", tournament_id)
    
    if Participant.objects.filter(tournament=tournament, user=request.user).exists():
        messages.error(request, "You have already registered.")
        return redirect("tournaments:tournament_detail", tournament_id)
    
    Participant.objects.create(tournament=tournament, user=request.user)
    messages.success(request, "You have successfully registered!")
    return redirect("tournaments:tournament_detail", tournament_id)

@staff_member_required
def generate_bracket_view(request, tournament_id):
    tournament=get_object_or_404(Tournament, id=tournament_id)

    if tournament.is_team_based:
        contestants = list(tournament.teams.all())
        contestant_type = "teams"
    else:
        contestants = list(tournament.participants.all())
        contestant_type = "participants"

    count = len(contestants)

    if count == 0:
        messages.error(request, "No contestants registered yet.Cannot generate matches.")
        return redirect("tournaments:tournament_detail", tournament_id=tournament.id)

    if count < 2:
        messages.error(request, f"At least 2 {contestant_type} are required. Currently: {count}.")
        return redirect("tournaments:tournament_detail", tournament_id=tournament.id)
    
    if tournament.matches.exists():
        messages.error(request, "Matches have already been generated for this tournament.")
        return redirect("tournaments:tournament_detail", tournament_id=tournament.id)
    
    from itertools import combinations
    pairs = list(combinations(contestants, 2))
    
    for a, b in pairs:
        if tournament.is_team_based:
            Match.objects.create(tournament=tournament, team1=a, team2=b)
        else:
            Match.objects.create(tournament=tournament, participant1=a.user, participant2=b.user)

    
    total=len(pairs)
    messages.success(request, f"Bracket generated successfully! {total} matches created.")
    return redirect("tournaments:tournament_detail", tournament_id=tournament.id)