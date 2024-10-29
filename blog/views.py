from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

posts = [
    {
        'title': 'Beautiful is better than ugly',
        'author': 'John Doe',
        'content': 'Beautiful is better than ugly',
        'published_at': 'October 1, 2022'
    },
    {
        'title': 'Explicit is better than implicit',
        'author': 'Jane Doe',
        'content': 'Explicit is better than implicit',
        'published_at': 'October 1, 2022'
    }
]


def home(request, *args, **kwargs):
    context = {
        'posts' : posts
    }
    title = {
        'title' : 'Personal Blog'
    }
    return render(request, 'blog/home.html', context=context)


def about(request, *args, **kwargs):
    return render(request, 'blog/about.html')