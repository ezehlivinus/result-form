from django.urls import path
from . import views

# app_name = 'result'
urlpatterns = [
    path('', views.index, name='index'),
    path('students/<int:pk>/', views.detail, name='detail'),
    # path('students/', views., name='search'),
    # path('phones/', views.phones_list, name='phones'),
]