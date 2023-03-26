from django.urls import path
from . import views
from .context_processors import *


#create url here
urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('profile/', views.user_profile, name='profile'),
    path('subscribe/', subscribe, name='subscribe'),
    # path('change_password/', views.change_password, name='change_password'),
    # path('profile/', views.profile, name='profile'),
    path('blog-list/', views.PostListView.as_view(), name='blog_list'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
#     path('faq/new/', faq_view, name='faq_new'),
    path('<pk>/update', views.UserProfileUpdateView.as_view(), name='update_profile'), 
    path('search/', views.search, name='search'), 
    path('lookbook/', views.lookbook, name='lookbook'), 

]
