from django.contrib import admin
from .models import Participant

# Register your models here.
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'tournament', 'registered_at']
    list_filter = ['tournament'] 

admin.site.register(Participant, ParticipantAdmin)