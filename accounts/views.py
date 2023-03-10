from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
#import for update view
from django.views.generic.edit import UpdateView
from .models import *
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'User signup successfully.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'User successfully login.')
            return redirect('profile')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


# def blog_list(request):
#     return render(request, 'blog-right-sidebar.html')

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.user = request.user
            fs.save()
            messages.success(request, 'User profile successfully updated.')
            return redirect('profile')
    else:
        form = UserProfileForm()
    return render(request, 'my-account.html', {'form': form})


class UserProfileUpdateView(UpdateView):
    # specify the model you want to use
    model = Profile
    template_name = "accounts/profile_update.html"
    # specify the fields
    fields = [
        "image",
        "phone",
        "date_of_birth",
        "receive_offer_from_our_partner",
        "title",
    ]
  
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"


class FAQListView(ListView):
    model = FAQ
    template_name = 'faqs-style1.html'
    context_object_name = 'faqs'



class PostListView(ListView):
    model = Post
    template_name = "blog-right-sidebar.html"
    context_object_name = 'posts'



def search(request):        
    if request.method == 'GET': # this will be GET now      
        search =  request.GET.get('q') # do some research what it does
        try:
            results = Post.objects.filter((Q(title__icontains=search)) | (Q(content__icontains=search)) | (Q(category__name__icontains=search)))# filter returns a list so you might consider skip except part
            return render(request,"search.html",{"results":results})
        except:
            pass

    else:
        return render(request,"search.html",{})