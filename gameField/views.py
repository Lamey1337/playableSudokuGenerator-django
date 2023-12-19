from django.shortcuts import render
from .models import *
from .sudoku import sudoku


def indexView(request):

    counter = list(range(9)) * 9

    values = SudokuPuzzle.objects.get(pk=2).puzzle
    values = values.split("_")
    values = [i if i != "0" else "" for i in values]

    context = {
        "lines": counter,
        "values": values,
        "changed": []
    }

    if request.method == "POST":

        changed = []
        field = request.POST.getlist("sudoku")
        for x,y in zip(values,field):
            if x == y: changed.append("")
            else: changed.append(y)
        context["changed"] = changed

        for i in field:
            if not i:
                context["item_missing"] = True
                return render(request, "gameField/test.html", context)   
            
        context["check"] = sudoku.Sudoku(field).check()
        
    return render(request, "gameField/test.html", context)

def testView(request):

    counter = list(range(9)) * 9

    values = SudokuPuzzle.objects.get(pk=4).puzzle
    values = values.split("_")
    values = [i if i != "0" else "" for i in values]

    context = {
        "lines": counter,
        "values": values,
        "changed": []
    }

    if request.method == "POST":

        changed = []
        field = request.POST.getlist("sudoku")
        for x,y in zip(values,field):
            if x == y: changed.append("")
            else: changed.append(y)
        context["changed"] = changed

        for i in field:
            if not i:
                context["item_missing"] = True
                return render(request, "gameField/test.html", context)   
            
        context["check"] = sudoku.Sudoku(field).check()
        
    return render(request, "gameField/test.html", context)

 