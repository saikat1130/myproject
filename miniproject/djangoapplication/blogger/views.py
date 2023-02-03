from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'blogs/index.html',{'posts'  :posts})

def user_login(request):
 if not request.user.is_authenticated:
    if request.method == 'POST':
      form = LoginForm(request=request,data=request.POST)
      if form.is_valid():
       uname = form.cleaned_data['username']
       upass = form.cleaned_data['password']
       user = authenticate(username=uname,password=upass)
       if user is not None:
        login(request,user)
        messages.success(request,'Logged in successfully')
        return HttpResponseRedirect('/dashboard/')
    else:
      form = LoginForm()
    return render(request, 'blogs/login.html',{'form':form})
 else:
  return HttpResponseRedirect('/dashboard/')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,'Registered Successfully')
            form.save()
    else :
        form = SignUpForm()
    return render(request, 'blogs/sign_up.html',{'form':form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def about(request):
    return render(request, 'blogs/about.html')

def contact(request):
    return render(request, 'blogs/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
     posts = Post.objects.all()
     user = request.user
     full_name = user.get_full_name()
     return render(request, 'blogs/dashboard.html',{'posts':posts,'full_name':full_name})
    else:
      return HttpResponseRedirect('/login/')


def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid:
                form.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request,'blogs/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def updatepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'blogs/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

def deletepost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return render(request,'/dashboard')
    else:
        return HttpResponseRedirect('/login/')