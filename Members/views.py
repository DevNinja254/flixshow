from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from  Members.form import Buyer
from django.contrib.auth.decorators import login_required
from flix.DRY import userDetails
from .models import DepositHistory, DownloadHistory,Onwatch, Buyers

import os
# Create your views here.

# Seller Registration process
def register(request):
    if request.method == 'POST':
    #   detailed form
      form = Buyer(request.POST)
      if form.is_valid():
        user = form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(email = email, password=password)
        auth_login(request, user)
        return redirect("/")
      
    else:
        # blank form
        form = Buyer()
    return render(request, 'registration.html',{'form': form})

# All Members Login form
def login(request): 
    if request.method == "POST": 
        # value form
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = auth_login(request, form.get_user())
            return redirect("/")
    else: 
        # blank form
        form = AuthenticationForm()
    return render(request, "login.html", { "form": form })

# All members Logout process
@login_required(login_url="/membership/login/")
def logout(request):
    #if request.method == "POST":settings
    user = request.user 
    # userDetails.last_login = datetime.now()
    auth_logout(request)
    return redirect('/')

@login_required(login_url="/membership/login/")
def dashboard(request):
    userDetailed = userDetails(request)["userBuyrDetailsDi"]
    userObject = Buyers.objects.get(username = userDetailed['username'])
    if request.method == "POST":
        print(userObject.username)
        profile = request.FILES.get("profile")
        userObject.username = request.POST["username"]
        userObject.email = request.POST["email"]
        userObject.phone_number = request.POST["phone_number"]
        userObject.country = request.POST["country"]
        userObject.city = request.POST["city"]
        if profile:
            userObject.profile = request.FILES.get("profile")
        userObject.save()
        return redirect("/membership/dashboard/")
    downloadHistory = DownloadHistory.objects.filter(name = userDetailed['username'])
    depositHistory = DepositHistory.objects.filter(name = userDetailed['username'])
    watch = Onwatch.objects.all().reverse()
    print(Buyers.objects.get(username = userDetailed['username']).profile)
    context = {
        "userDetail":userDetailed,
        "downloadHistory":downloadHistory.reverse(),
        "depositHistory":depositHistory.reverse(),
        "watch":watch,
        "userObject":userObject
    }
    return render(request, "dashboard.html", {"context": context})

@login_required(login_url="/membership/login/")
def setting(request):

    return render(request, "setting.html")

# pass
# word
# reset
