# I have created this file
from string import punctuation

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(name, email, message)
    return render(request, 'contact.html')

def analyze(request):
    djtext = request.POST.get('text', 'default')

    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charcount = request.POST.get('charcount', 'off')

    analyzed = djtext
    purpose = []

    if removepunc == 'on':
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        temp = ""
        for char in analyzed:
            if char not in punctuations:
                temp += char
        analyzed = temp
        purpose.append("Removed Punctuations")

    if fullcaps == 'on':
        analyzed = analyzed.upper()
        purpose.append("Uppercase")

    if newlineremover == 'on':
        temp = ""
        for char in analyzed:
            if char != "\n" and char != "\r":
                temp += char
        analyzed = temp
        purpose.append("Removed New Lines")

    if extraspaceremover == 'on':
        temp = ""
        for index, char in enumerate(analyzed):
            if index < len(analyzed) - 1:
                if not (analyzed[index] == " " and analyzed[index + 1] == " "):
                    temp += char
            else:
                temp += char
        analyzed = temp
        purpose.append("Extra Space Removed")

    if charcount == 'on':
        count = len(analyzed)
        analyzed += f"\n\nTotal Characters: {count}"
        purpose.append("Character Count")

    if not purpose:
        return HttpResponse("Error: Please select at least one operation")

    params = {
        'purpose': ", ".join(purpose),
        'analyzed_text': analyzed
    }

    return render(request, 'analyze.html', params)