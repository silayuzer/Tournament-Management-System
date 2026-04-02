from django.contrib import admin
from .models import Tournament, Match
from teams.models import Team
from participants.models import Participant

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    verbose_name = "Individual Contestant"
    verbose_name_plural = "Individual Contestants"
    fields = ['user']

class TeamInline(admin.TabularInline):
    model = Team
    extra = 0
    verbose_name = "Team Contestant"
    verbose_name_plural = "Team Contestants"
    fields = ['name', 'captain', 'created_by']

class MatchInline(admin.TabularInline):
    model = Match
    extra = 0

    def get_fields(self, request, obj = None):
        if obj and obj.is_team_based:
            return ['team1', 'team2', 'winner_team']
        return ['participant1', 'participant2', 'winner_participant'] 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        tournament_id = self._get_tournament_id(request)

        if tournament_id:
            if db_field.name in ('team1', 'team2'):
                kwargs['queryset'] = Team.objects.filter(tournament_id=tournament_id)

            if db_field.name in ('participant1', 'participant2', 'winner_participant'):
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user_ids = Participant.objects.filter(tournament_id=tournament_id).values_list('user_id', flat=True)
                kwargs['queryset'] = User.objects.filter(id__in=user_ids)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
            tournament_id = self._get_tournament_id(request)

            if db_field.name == 'winner_participant':
                if tournament_id:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_ids = Participant.objects.filter(tournament_id=tournament_id).values_list('user_id', flat=True)
                    kwargs['queryset'] = User.objects.filter(id__in=user_ids)

                if db_field.name in ('team1', 'team2', 'winner_team'):
                    if tournament_id:
                        kwargs['queryset'] = Team.objects.filter(tournament_id=tournament_id)

                if db_field.name in ('participant1', 'participant2'):
                    if tournament_id:
                        from django.contrib.auth import get_user_model
                        User = get_user_model()
                        user_ids = Participant.objects.filter(tournament_id=tournament_id).values_list('user_id', flat=True)
                        kwargs['queryset'] = User.objects.filter(id__in=user_ids)
                
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
    def _get_tournament_id(self, request):
        try:
            path_parts = request.path.split('/')
            idx = path_parts.index('tournament') 
            return int(path_parts[idx + 1])
        except (ValueError, IndexError):
            return None

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'discipline', 'start_time', 'is_active']
    list_filter = ['discipline', 'is_active']
    
    def get_inlines(self, request, obj=None):
        if obj is None:
            return []
        if obj.is_team_based:
            return [TeamInline, MatchInline]
        return [ParticipantInline, MatchInline]
    
    def get_fields(self, request, obj = None):
        base = ['name', 'discipline', 'organizer', 'description', 'start_time', 'location', 'application_deadline', 'is_active']
        if obj is None:
            return base + ['max_teams', 'max_participants']
        if obj.is_team_based:
            return base + ['max_teams']
        return base + ['max_participants']


class MatchAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'tournament', 'get_winner']
    list_filter = ['tournament']

    def get_winner(self, obj):
        if obj.tournament.is_team_based:
            return obj.winner_team
        return obj.winner_participant
    get_winner.short_description = 'Winner'

    def get_fields(self, request, obj = None):
        if obj and obj.tournament.is_team_based:
            return ['tournament', 'team1', 'team2', 'winner_team']
        return ['tournament', 'participant1', 'participant2', 'winner_participant']
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj_id = request.resolver_match.kwargs.get('object_id')
        if obj_id:
            try:
                match = Match.objects.select_related('tournament').get(pk=obj_id)
                tournament = match.tournament
                if db_field.name in ('team1', 'team2', 'winner_team'):
                    kwargs['queryset'] = Team.objects.filter(tournament=tournament)

                if db_field.name in ('participant1', 'participant2'):
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_ids = Participant.objects.filter(tournament=tournament).values_list('user_id', flat=True)
                    kwargs['queryset'] = User.objects.filter(id__in=user_ids)

                if db_field.name == 'winner_participant':
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    allowed = []
                    if match.participant1:
                        allowed.append(match.participant1.pk)
                    if match.participant2:
                        allowed.append(match.participant2.pk)
                    kwargs['queryset'] = User.objects.filter(pk__in=allowed)

                if db_field.name == 'winner_team':
                    allowed = []
                    if match.team1:
                        allowed.append(match.team1.pk)
                    if match.team2:
                        allowed.append(match.team2.pk)
                    kwargs['queryset'] = Team.objects.filter(pk__in=allowed)

            except Match.DoesNotExist:
                pass
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Match, MatchAdmin)