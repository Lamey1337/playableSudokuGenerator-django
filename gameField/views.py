from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .sudoku import sudoku


def indexView(request):

    if request.method == "POST":

        id = request.POST["selected"]
        if request.POST.get("delete"):
            SudokuPuzzle.objects.get(id=id).delete()
            return redirect("index")

        return redirect("puzzle", pk = id)
    

    idList = SudokuPuzzle.objects.values_list("id", flat=True)

    context = {
        "idList": idList,
    }


        
    return render(request, "gameField/index.html", context)

def puzzleView(request, pk):
    
    counter = list(range(9)) * 9

    values = get_object_or_404(SudokuPuzzle, pk=pk).puzzle
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
                context["item_missing"] = "notReady"
                return render(request, "gameField/puzzle.html", context)
                 
        context["check"] = sudoku.Sudoku(field).check()
        context["item_missing"] = "ready"

    return render(request, "gameField/puzzle.html", context)

def newPuzzleView(requst):

    newPuzzle = sudoku.genSudoku().puzzle()
    newPuzzle = "_".join(newPuzzle)
    new = SudokuPuzzle(puzzle=newPuzzle)
    new.save()

    return redirect("index")