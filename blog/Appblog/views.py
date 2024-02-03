from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .models import Post, Comment
from .forms import UserCreationForm, LoginForm, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.

def home(request):
    post = Post.objects.all().order_by("-created_on")
    
    context={'posts':post}
    return render(request, 'blog/index.html', context)

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
    }

    return render(request, "blog/detail.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(post=post).order_by("-created_on")
    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
    }
    return render(request, "blog/detail.html", context)

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            usrename =form.cleaned_data['username']
            messages.success(request, f"{usrename} successfully registered!")
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form':form}
    return render(request, 'blog/signup.html', context)

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    

                messages.success(request, "logged in succcessfully!")

                return redirect('home')
    else:
        form = LoginForm()
    
    context = {'form':form}
    return render(request, 'blog/login.html',context)

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
