import random
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Tournament, Match
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
    teams=Team.objects.filter(tournament=tournament)
    matches=Match.objects.filter(tournament=tournament)

    can_register=(
        request.user.is_authenticated and
        timezone.now() < tournament.application_deadline and
        teams.count() < tournament.max_teams
    )

    return render(request, "tournaments/tournament_detail.html", {
        "tournament": tournament, 
        "teams": teams, 
        "matches": matches
    },)
@staff_member_required
def generate_bracket_view(request, tournament_id):

    tournament=get_object_or_404(Tournament, id=tournament_id)
    
    if tournament.matches.exists():
        messages.error(request, "Matches have already been generated for this tournament.")
        return redirect("tournaments:tournament_detail", tournament_id=tournament.id)
    
    teams= list(Team.objects.filter(tournament=tournament))

    if len(teams) < 2:
        messages.error(request, "Not enough teams to generate a bracket.")
        return redirect("tournaments:tournament_detail", tournament_id=tournament.id)
    
    random.shuffle(teams)
    
    for i in range(0, len(teams)-1, 2):
        Match.objects.create(
            tournament=tournament,
            team1=teams[i],
            team2=teams[i+1]
        )
    messages.success(request, "Bracket generated successfully.")
    return redirect("tournaments:tournament_detail", tournament_id=tournament.id)