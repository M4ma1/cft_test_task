from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.module import *

# Create your views here.

def home(request):
    return render(request, "index.html")

@csrf_exempt
def check_repo(request):
    if is_string_an_url(request.POST['inputString']):
        send_to_queue(request.POST['inputString'])
    
        return render(request, "ok.html")
    else:
        return render(request, "bad.html")