from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog
# Create your views here.

posts = Blog.objects.all()


def home(request, *args, **kwargs):
    context = {
        'posts' : posts
    }
    
    return render(request, 'blog/home.html', context=context)


def about(request, *args, **kwargs):
    context = {
        "name" : "Alec",
        "number" : '8967-465-72-75',
        'address' : 'A.Qodiriy 54/16'
    }
    return render(request, 'blog/about.html', context=context)