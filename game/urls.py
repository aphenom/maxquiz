from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("start/", views.start, name="start"),
    path("api/answer/", views.answer, name="answer"),
    path("api/joker/", views.joker, name="joker"),
    path("api/abandon/", views.give_up, name="give_up"),
    path("classement/", views.leaderboard, name="leaderboard"),
    path("portefeuille/", views.wallet, name="wallet"),
    path("api/space-answer/", views.space_answer, name="space_answer"),
    path("e/<slug:slug>/", views.space_home, name="space_home"),
    path("e/<slug:slug>/jouer/", views.space_start, name="space_start"),
    path("e/<slug:slug>/tableau-de-bord/", views.space_dashboard, name="space_dashboard"),
]
