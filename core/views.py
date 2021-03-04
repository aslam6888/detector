from django.shortcuts import render,redirect
from .models import video
from data.demo_usage import detect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

# Create your views here.
@login_required(login_url='/login_page')
def home(request):
    vid=video.objects.filter(user=request.user)
    with open("data\coco.names", 'r') as f:
        classes = [w.strip() for w in f.readlines()]
    selected={}
    if request.method=="POST":
        obj=request.POST.getlist('objects')
        for data in obj:
            selected[data] =(0,255,255)
        files=video(user=request.user,video=request.FILES['video'])
        files.save()
        detect(selected,files)
        return redirect('/download')
    context={'classes':classes,'video':vid}
    return render(request,"index.html",context)
@login_required(login_url='/login_page')
def download(request):
    return render(request,'download.html')

@login_required(login_url='/login_page')
def delete(request):
    vid=video.objects.filter(user=request.user)
    vid.delete()
    return redirect('/')

def login_page(request):
    username =request.POST.get('uname')
    password=request.POST.get('psw')
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('/')
    return render(request,'login.html')

def logoutview(request):
    logout(request)
    return redirect('/login_page') 

    