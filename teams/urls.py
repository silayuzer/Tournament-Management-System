from django.urls import path
from .views import register_team

app_name = "teams"

urlpatterns = [
    path("register/<int:tournament_id>/", register_team, name="register_team"),
]