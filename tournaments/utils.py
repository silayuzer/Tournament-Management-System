import random
from .models import Match

def generate_bracket(tournament):
    if tournament.is_team_based:
        from teams.models import Team
        contestants = list(Team.objects.filter(tournament=tournament))
    else:
        from .models import Participant
        contestants = list(tournament.participants.all())
    
    if len(contestants) < 2:
        raise ValueError("Not enough contestants to generate a bracket")
    
    if len(contestants) % 2 != 0:
        raise ValueError("Number of contestants must be even")

    if Match.objects.filter(tournament=tournament).exists():
        raise ValueError("Matches have already been generated")
    

    random.shuffle(contestants)
    for i in range(0, len(contestants), 2):
        if tournament.is_team_based:
            Match.objects.create(
                tournament=tournament,
                team1=contestants[i],
                team2=contestants[i+1]
            )
        else:
            Match.objects.create(
                tournament=tournament,
                participant1=contestants[i].user,
                participant2=contestants[i+1].user
            )