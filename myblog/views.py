from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
from .forms import InputForm

def index(request):
    if request.method == 'POST':
        form = InputForm(request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myblog/result.html')
        else:
            print(form.is_valid())
            print(form)

    form = InputForm()
    data = {
        'form': form
    }

    return render(request, 'myblog/main.html', data)

def result(request):
    return render(
        request,
        'myblog/result.html',
    )