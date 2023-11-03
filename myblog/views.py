from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

def main(request):
        return render(
            request,
            'myblog/main.html'
        )

def result(request):
    return render(
        request,
        'myblog/result.html'
    )

def data(request):
    return HttpResponse("<input type='file' class='addfile' accept='.txt,.json'>")