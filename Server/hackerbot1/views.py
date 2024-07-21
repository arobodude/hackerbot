from django.shortcuts import render
import hackerbot1.hackerbot_commands as hb
import sys
from django.http import JsonResponse
import threading

def hackbot_command(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        print("Button was clicked!", file=sys.stdout)
        hb.send_command(input_text)

def send_command(request):
    if request.method == 'POST':
        text = request.POST.get('text_input')
        hackbot_command(text)
        return JsonResponse({'status': 'Processing started'})
    return JsonResponse({'status': 'Invalid request'}, status=400)

def home(request):
    return render(request, 'home.html')