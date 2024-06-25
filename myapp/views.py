from django.shortcuts import render
from myapp.models import Data

def index(request):
    data =  Data.objects.all()
    return render(request, "index.html", {"room_name": "test", "data":data})