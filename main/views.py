from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World / Sessions Application (53a9b4c9)<br><a href='/hello/'>/hello/</a><br><a href='/polls/owner'>/polls/owner</a>")
