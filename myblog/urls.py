from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.main, name = 'main'),
    path('input_1/', views.input_1, name = 'input_1'),
    path('input_2/', views.input_2, name = 'input_2'),
    path('input_3/', views.input_3, name = 'input_3'),
    path('input_4/', views.input_4, name = 'input_4'),
    path('input_5/', views.input_5, name = 'input_5'),
    path('result_1/', views.result_1, name = 'result_1'),
    path('result_2/', views.result_2, name = 'result_2'),
    path('result_3/', views.result_3, name = 'result_3'),
    path('result_4/', views.result_4, name = 'result_4'),
    path('result_5/', views.result_5, name = 'result_5'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)