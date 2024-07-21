from django.shortcuts import render
import hackerbot.hackerbot_commands as hb
import sys
from django.http import JsonResponse


def hackbot_command(command):
    print("Button was clicked!", file=sys.stdout)
    hb.send_command(command)


def send_command(request):
    if request.method == 'POST':
        text = request.POST.get('text_input')
        hackbot_command(text)
        return JsonResponse({'status': 'Processing started'})
    return JsonResponse({'status': 'Invalid request'}, status=400)


def send_move_command(request):
    if request.method == 'POST':
        x_coord = request.POST.get("x_coord")
        y_coord = request.POST.get("y_coord")
        angle = request.POST.get("angle")
        speed = request.POST.get("speed")
        command = f"GOTO,{x_coord},{y_coord},{angle},{speed}"
        hackbot_command(command)
        return JsonResponse({'status': 'Processing started'})
    return JsonResponse({'status': 'Invalid request'}, status=400)


def home(request):
    return render(request, 'home.html')