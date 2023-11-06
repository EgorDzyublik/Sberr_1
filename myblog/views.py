from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
import pandas as pd
#from myblog.progr.alg import func

def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result')
    return render(request, 'myblog/main.html')

def result(request):
    result =
    amount = len(result)
    return render(request,'myblog/result.html', {'result': result}, {'amount': amount})