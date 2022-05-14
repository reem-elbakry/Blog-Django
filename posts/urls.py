from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts),
    path('post/<int:id>',views.post_detail),
    path('subscribe/<cat_id>', views.subscribe),
    path('unsubscribe/<cat_id>', views.unsubscribe),
]    	


    
