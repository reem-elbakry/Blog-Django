from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts),
    path('post/<int:id>',views.post_detail),
    path('subscribe/<cat_id>', views.subscribe),
    path('unsubscribe/<cat_id>', views.unsubscribe),
    path('createPost/', views.createPost),
    path('category/<cat_id>', views.categoryPosts),
    path('tag/<tag_id>', views.tagPosts),
    path('search', views.search),
    path('updatepost/<id>',views.post_update),
    path('delpost/<num>',views.post_delete),    	

]    	


    
