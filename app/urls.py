from django.urls import path 
from .views import login_view,logout_view,signup_view,HomeView,ArticleDetailView,AddPostView,UpdatePostView,DeletePostView,AddCategoryView,CategoryView,LikeView,UserProfileView,UserEditView


urlpatterns=[
# path('home/',base,name='home'),
path('login/',login_view,name='login'),
path('logout/',logout_view,name='logout'),
path('signup/',signup_view,name='signup'),
path('',HomeView.as_view(),name='home'),
path('article/<int:pk>/',ArticleDetailView,name='ac'),
path('add_post/',AddPostView.as_view(),name='add_post'),
path('article_edit/<int:pk>',UpdatePostView.as_view(),name='update_post'),
path('article_edit/<int:pk>/remove',DeletePostView.as_view(),name='delete_post'),
path('add_category/',AddCategoryView.as_view(),name='add_category'),
path('category/<str:cats>/',CategoryView,name='category'),
path('like/<int:pk>',LikeView,name='like_post'),
path('profile/',UserProfileView,name='profile'),
path('edit_profile/<int:pk>',UserEditView,name='edit_profile')
]