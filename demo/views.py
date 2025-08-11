from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("This is a testing page.\n"+
                        "There's nothing here temporarily.")
