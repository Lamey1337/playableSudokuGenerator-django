from django.db import models

# Create your models here.

class SudokuPuzzle(models.Model):
    puzzle = models.CharField(max_length=200)

    def __str__(self) -> str:
        return str(self.id)

