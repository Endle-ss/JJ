from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def cards(request):
    return render(request, 'main/cards.html')
