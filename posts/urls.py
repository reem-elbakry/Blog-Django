from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts),
    path('post/<int:id>',views.post_detail),
    path('subscribe/<cat_id>', views.subscribe),
    path('createPost/', views.createPost, name='create'),
    path('category/<cat_id>', views.categoryPosts),
    path('tag/<tag_id>', views.tagPosts),
]    	


    
