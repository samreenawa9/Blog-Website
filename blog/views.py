from email import message
from django.http import HttpResponse
from .models import Post,ContactMessage
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-published_at')
    return render(request, 'blog.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("Name")
        phone= request.POST.get("Phone")
        email=request.POST.get("Email")
        message=request.POST.get("Message")
        
        ContactMessage.objects.create(name=name,phone=phone,email=email,message=message)
        # messages.success(request,"Your messege has been sent")
        return redirect("contact")
    return render(request, 'contact.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')  # Redirect superusers/staff to Django admin
            else:
                return redirect('home')  # Redirect normal users to home
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login.html')

