from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.newRoom),
    path('get/<room_code>', views.getRoom),
    path('getAll/', views.getAllRoom),
    path('run/<room_code>', views.runRoom),
    path('close/<room_code>', views.closeRoom),
]