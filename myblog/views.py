from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView
import pandas as pd
from media.alg_clustering import groups_clusters
from media.alg_first import groups_alg1
from media.alg_smart import groups_alg_smart
from media.alg_style import groups_alg_author_style
from media.alg_metrics_linear_model import groups_metrics
import json
import os

def main(request):
    return render(request, 'myblog/main.html')

def input_1(request):
    if os.path.isfile('media/sample_test'):
        os.remove('media/sample_test')
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        uploaded_file.name = 'sample_test'
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result_1')
    return render(request, 'myblog/input_1.html')

def input_2(request):
    if os.path.isfile('media/sample_test'):
        os.remove('media/sample_test')
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        uploaded_file.name = 'sample_test'
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result_2')
    return render(request, 'myblog/input_2.html')

def input_3(request):
    if os.path.isfile('media/sample_test'):
        os.remove('media/sample_test')
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        uploaded_file.name = 'sample_test'
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result_3')
    return render(request, 'myblog/input_3.html')

def input_4(request):
    if os.path.isfile('media/sample_test'):
        os.remove('media/sample_test')
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        uploaded_file.name = 'sample_test'
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result_4')
    return render(request, 'myblog/input_4.html')

def input_5(request):
    if os.path.isfile('media/sample_test'):
        os.remove('media/sample_test')
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        uploaded_file.name = 'sample_test'
        fs.save(uploaded_file.name, uploaded_file)
        return redirect('/result_5')
    return render(request, 'myblog/input_5.html')


def result_1(request):

    with open('media/sample_test', encoding="utf-8") as sber_file:
        f = json.load(sber_file)

    result = alg_first.groups_alg1(f)
    return render(request,'myblog/result.html', {'result': result})

def result_2(request):

    with open('media/sample_test', encoding="utf-8") as sber_file:
        f = json.load(sber_file)

    result = alg_clustering.groups_clusters(f)
    return render(request,'myblog/result.html', {'result': result})

def result_3(request):

    with open('media/sample_test', encoding="utf-8") as sber_file:
        f = json.load(sber_file)

    result = alg_metrics_linear_model.groups_metrics(f)
    return render(request,'myblog/result.html', {'result': result})

def result_4(request):

    with open('media/sample_test', encoding="utf-8") as sber_file:
        f = json.load(sber_file)

    result = alg_smart.groups_alg_smart(f)
    return render(request,'myblog/result.html', {'result': result})

def result_5(request):

    with open('media/sample_test', encoding="utf-8") as sber_file:
        f = json.load(sber_file)

    result = alg_style.groups_alg_author_style(f)
    return render(request,'myblog/result.html', {'result': result})