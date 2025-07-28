from django.urls import path
from . import views

app_name = 'initial_audit'

urlpatterns = [
    path('', views.index, name='index'),
    path('view/', views.corp_view, name ='view'),
]