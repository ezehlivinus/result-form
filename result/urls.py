from django.urls import path
from . import views

# app_name = 'result'
urlpatterns = [
    path('', views.index, name='index'),
    path('students/<int:pk>/', views.detail, name='detail'),
    path('students/<int:pk>/edit/', views.edit, name='edit'),
    path('students/<int:pk>/subjects/<int:subject_id>/', views.submit_result, name='submit_result'),
    # path('invoice/', views.GeneratePdf.as_view(), name='search'),
    # path('phones/', views.phones_list, name='phones'),
]