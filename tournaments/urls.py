from django.urls import path
from . import views
from .views import create_tournament

app_name = "tournaments"
urlpatterns = [
    path("", views.tournament_list, name="list"),
    path("tournament/<int:tournament_id>/", views.tournament_detail, name="tournament_detail"),
    path("tournament/<int:tournament_id>/generate/", views.generate_bracket_view, name="generate_bracket"),
    path("create/", views.create_tournament, name="create_tournament"),
]