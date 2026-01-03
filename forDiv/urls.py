from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('login',views.login),
    path('main',views.main),
    path('del',views.delete),
    path('register',views.register),
    path('askds',views.askds),
    path('info',views.info),
    path('baidumap',views.baidumap),
    path('route', views.get_route),
    path('authstatus',views.authstatus),
    path('modifypwd',views.modifypwd),
    path('uploadimg',views.uploadimg),
    path('postmusic',views.postmusic),
    path('getmusic',views.getmusic),
    path('deletemusic',views.deletemusic),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
]