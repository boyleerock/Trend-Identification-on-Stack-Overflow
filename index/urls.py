from django.urls import path
from index import views

urlpatterns = [
    path('', views.index),
    path('per_denied', views.per_denied)
    # path('timeWindows/', views.timeWindows),
]