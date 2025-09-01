from django.urls import path

from . import views

urlpatterns = [
    path('index/<str:usname>',views.index,name='index'),
    path('dlt',views.for_delete),
    path('login',views.login,name='login'),
    path('askds',views.askds,name='askds'),
    path('',views.redir),
    path('outer',views.outer),
]