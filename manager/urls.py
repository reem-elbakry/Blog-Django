from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("admins/", views.admins, name="admins"),
    path("admins/show/<int:id>", views.show, name="show_admin"),
    path("admins/lock/<int:id>", views.lock_admin, name="lock_admin"),

]
