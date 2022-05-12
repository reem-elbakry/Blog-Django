from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("users/", views.users, name="users"),
    path("admins/", views.admins, name="admins"),
    path("admins/show/<int:id>", views.show, name="show_admin"),
    path("admins/lock/<int:id>", views.lock_admin, name="lock_admin"),
    path("admins/unlock/<int:id>", views.unlock_admin, name="unlock_admin"),
    path("admins/delete/<int:id>", views.delete_admin, name="delete_admin"),
    path("admins/demote/<int:id>", views.demote, name="demote"),
    path("users/promote/<int:id>/", views.promote, name="promote"),
    path("users/show/<int:id>/", views.show, name="show"),



]
