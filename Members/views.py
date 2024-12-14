from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import logout as auth_logout, login as auth_login
from  Members.form import Buyer
from rest_framework import serializers
from django.contrib.auth.decorators import login_required
from flix.DRY import userDetails
from .models import DepositHistory, DownloadHistory
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Members
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import PasswordReset
import os
# Create your views here.

# Seller Registration process
def register(request):
    if request.method == 'POST':
    #   detailed form
      form = Buyer(request.POST)
      if form.is_valid():
         form.save()
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
            return redirect("/", {"user": user})
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
    downloadHistory = DownloadHistory.objects.filter(name = userDetailed['username'])
    depositHistory = DepositHistory.objects.filter(name = userDetailed['username'])
    context = {
        "userDetail":userDetailed,
        "downloadHistory":downloadHistory,
        "depositHistory":depositHistory,
    }
    return render(request, "dashboard.html", {"context": context})

@login_required(login_url="/membership/login/")
def setting(request):

    return render(request, "setting.html")

# pass
# word
# reset
