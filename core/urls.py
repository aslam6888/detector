from django.urls import path
from . import views
urlpatterns=[
    path('',views.home),
    path('download',views.download),
    path('delete',views.delete),
    path('login_page',views.login_page),
    path('logout',views.logoutview)
]