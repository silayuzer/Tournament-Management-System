from django.urls import path
from tournaments import views

app_name = "participants"

urlpatterns = [
    path("join/<int:tournament_id>/", views.register_participant, name="register_participant"),
]