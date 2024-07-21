from django.shortcuts import render
import hackerbot1.hackerbot_commands as hb
import sys

def print_command(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        print("Button was clicked!", file=sys.stdout)
        hb.send_command(input_text)
    else:
        print("No message sent")



def home(request):
    return render(request, 'home.html')