import random
from .models import Match
from teams.models import Team

def generate_bracket(tournament):
    teams = list(Team.objects.filter(tournament=tournament))
    random.shuffle(teams)

    if len(teams) < 2:
        raise ValueError("Not enough teams to generate a bracket")
    if len(teams) % 2 != 0:
        raise ValueError("Number of teams must be even")
    
    if Match.objects.filter(tournament=tournament).exists():
        raise ValueError("Matches have already been generated for this tournament")
    
    random.shuffle(teams)
    for i in range(0, len(teams), 2):
        Match.objects.create(
            tournament=tournament,
            team1=teams[i],
            team2=teams[i+1] 
        )