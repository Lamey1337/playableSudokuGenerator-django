from django.urls import path
from .views import *

urlpatterns = [
    path("", indexView, name="index"),
    path("puzzle/<int:pk>", puzzleView, name="puzzle"),
    path("newPuzzle", newPuzzleView, name="newPuzzle")
]
