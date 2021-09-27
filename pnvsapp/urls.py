from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('pc',views.pc, name='pc'),
    path('recoup',views.recoup,name='recoup')
]