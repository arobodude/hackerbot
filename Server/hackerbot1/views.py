from django.shortcuts import render
import hackerbot1.hackerbot_commands as hb
import sys
from django.http import JsonResponse

def print_command(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        print("Button was clicked!", file=sys.stdout)
        hb.send_command(input_text)
        return JsonResponse({'status': 'success', 'message': 'Command executed.'})
    return JsonResponse({'status': 'failure', 'message': 'Invalid request.'})



def home(request):
    return render(request, 'home.html')