# see https://github.com/NUDelta/sig-command/tree/main (git push origin2)

from django.shortcuts import render
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

def find_sig(sig_abbr, studio_info):
    for sig in studio_info:
        if sig['abbreviation'].lower().strip() == sig_abbr.lower().strip():
            return sig
    return None

@csrf_exempt
def index(request):
    print("in sig request")

    f = open('studioInfo.json')
    studio_info = json.load(f)

    sig_list = []
    for sig in studio_info:
        sig_list.append(sig['abbreviation'])

    sig_abbr = request.POST["text"]
    sig = find_sig(sig_abbr, studio_info)
    if not sig:
        return HttpResponse("Sorry that is not a SIG. The SIGs are " + ", ".join(sig_list))
    projects = sig['projects']

    content = ""
    for project in projects:
        content += "*" + project['project_name']
        for student in project['students']:
            content += " - " + student
        content += "*\n"

        # Sprint Log
        if project['documents']['Sprint Log'].strip():
            content += "Sprint Log:\n"
            content += project['documents']['Sprint Log'] + "\n"

        # Practical Research Canvas
        if project['documents']['Practical Research Canvas'].strip():
            content += "Practical Research Canvas:\n"
            content += project['documents']['Practical Research Canvas'] + "\n"

        # Research Research Canvases
        if project['documents']['Research Research Canvas'].strip():
            content += "Research Research Canvas:\n"
            content += project['documents']['Research Research Canvas'] + "\n"

        # IPM

        # Weekly
        content += '\n'

    # details about slack command that will trigger this info https://api.slack.com/apps/AJ3T9KU84/slash-commands?

    # used https://dashboard.ngrok.com/get-started to forward

    return JsonResponse({'text': content, 'response_type': 'in_channel'})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
