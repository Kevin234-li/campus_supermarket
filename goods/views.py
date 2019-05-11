from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def index(request):
    user = User()
    user.id = 1
    user.username = 'Kevin'
    return render(request, 'base.html', {'user': None})
    # return HttpResponse("Hello, Django")




