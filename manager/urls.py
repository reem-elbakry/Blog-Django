from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path("admins/delete/<int:id>", views.delete_admin, name="delete_admin"),
    path("admins/show/<int:id>", views.show, name="show_admin"),
]
