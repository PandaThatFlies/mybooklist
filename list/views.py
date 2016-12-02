from django.shortcuts import render, redirect,render_to_response
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from . import bookSearch
from . import models
import json


# Create your views here.
def home_page(request):
    return render(request,"home_page.html",{"user":request.user.username})

def search_results(request):
    if request.method == 'POST':
        searchWord=request.POST.get('searchWord', None)
        search=bookSearch.gbooks()
        resultList=search.search(searchWord)
        if request.user.is_authenticated():
            book_list=models.UserProfile.objects.filter(user_id=request.user.id)[0]
            return render(request,"search_results.html",{"resultList":resultList,"book_list":json.loads(book_list.book_list)})
        else:
            return render(request,"search_results.html",{"resultList":resultList})

    return HttpResponse("<h1>Use post</h1>")

def login_page(request):
    if(request.user.id!=None):
        return redirect("home_page")
    if request.method == 'POST':
        if request.POST.get("login"):
            username=request.POST.get('logUsername', None)
            password=request.POST.get('logPassword', None)
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect("home_page")
            else:
                return HttpResponse("Wrong username/password")              
        elif request.POST.get("signup"):
            username=request.POST.get('regUsername', None)
            password=request.POST.get('regPassword', None)
            confpasswprd=request.POST.get('confPassword', None)
            email=request.POST.get('regEmail', None)
            if(confpasswprd!=password):
                return HttpResponse("Passwords didn't match")
            try:
                user_exists = User.objects.get(username=username)
                return HttpResponse("Username already taken")
            except User.DoesNotExist:
                user = User.objects.create_user(username, email)
                user.set_password(password)
                user.save()
                book_list=models.UserProfile(user_id=user.id,book_list=json.dumps([]))
                book_list.save()
                user = authenticate(username=username,password=password)
                login(request, user)
                return redirect("home_page")
    return render(request,"login.html")

def list_page(request):
    if(request.user.id==None):
        return redirect("login")
    if request.method == 'POST':
        if request.POST.get("add_list"):
            book_id=request.POST.get('book_id', None)
            book_list=models.UserProfile.objects.filter(user_id=request.user.id)[0]
            new_list=json.loads(book_list.book_list)
            new_list.append(book_id)
            book_list.book_list=json.dumps(new_list)
            book_list.save()
        if request.POST.get("remove_list"):
            book_id=request.POST.get('book_id', None)
            book_list=models.UserProfile.objects.filter(user_id=request.user.id)[0]
            id_list=json.loads(book_list.book_list)
            for id in id_list:
                if id == book_id:
                    id_list.remove(book_id)
            book_list.book_list=json.dumps(id_list)
            book_list.save()

    id_list=json.loads(models.UserProfile.objects.filter(user_id=request.user.id)[0].book_list)
    book_list=[]
    fetch=bookSearch.gbooks()
    for id in id_list:
        book_list.append(fetch.getBook(id))
    return render(request,"list_page.html",{"book_list":book_list})

def testing(request):
    return HttpResponse("s")