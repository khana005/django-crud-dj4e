from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. 53a9b4c9 is the polls index.")

def owner(request):
    return HttpResponse("Hello, world. 53a9b4c9 is the polls owner.")
