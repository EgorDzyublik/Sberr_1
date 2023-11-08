from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
import pandas as pd
from media.alg import groups
import json
import os

def index(request):
    if os.path.isfile('media/sample_test'):
        os.remove('media/sample_test')
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        uploaded_file.name = 'sample_test'
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result')
    return render(request, 'myblog/main.html')

def result(request):

    with open('media/sample_test', encoding="utf-8") as sber_file:
        f = json.load(sber_file)

    result = groups(f)[1]
    amount = len(result)
    return render(request,'myblog/result.html', {'result': result, 'amount': amount})