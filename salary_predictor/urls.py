from django.urls import path
from . import views

urlpatterns = [
    path('predict_salary/', views.ml, name='predict_salary'),
]

