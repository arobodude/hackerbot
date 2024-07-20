from django.shortcuts import render
from django.http import HttpResponse
import sys

def print_command(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        print("Button was clicked!", file=sys.stdout)
        return HttpResponse("Button Clicked with text")
    return HttpResponse("Button was clicked No text")



def home(request):
    return render(request, 'home.html')