from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def singin(request):
    return render(request, 'pantallas/singin.html')
