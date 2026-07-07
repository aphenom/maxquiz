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
]
