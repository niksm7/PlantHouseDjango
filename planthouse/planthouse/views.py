from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from accounts.models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from shop.models import Cart
from nursery.models import Nursery
import string

def index(request):
    if request.user.is_authenticated:
        if request.user.is_nurseryManager:
            return redirect('/nursery')
        else:
            return redirect('/shop')
    return render(request,'index.html')

def handleSignup(request):
    if request.method == "POST":
        #get the post parameters
        emailSignup = request.POST['emailSignup']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        isManager = request.POST.get('ismanager','no')
        if isManager == "yes":
            nurseryname = request.POST.get('nurseryname')
        
        # check for errorneous inputs
        if Account.objects.filter(email=emailSignup).exists():
            messages.error(request,'Email already taken please choose some other username')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if Account.objects.filter(username=username).exists():
            messages.error(request,'Username already taken please choose some other username')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if len(username)>10:
            messages.error(request, 'Username must be under 10 characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if not username.isalnum():
            messages.error(request,'Username must only contain alpha numeric characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        
        if len(pass1)<8:
            messages.error(request,"Password must contain atleast 8 characters")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


        #Create the user
        password = make_password(pass1)
        if isManager == "yes": 
            myuser = Account(email=emailSignup,username=username,password=password,is_nurseryManager=True,nursery_name=nurseryname)

            #When a nursery manage has signed up and the nursery name doesn't exists add the nursery name to Nursery Model.

            if not(Nursery.objects.filter(name=nurseryname).exists()):
                nursery = Nursery(name=nurseryname)
                nursery.save()
        else:
            myuser = Account(email=emailSignup,username=username,password=password)
        myuser.save()

        #When new user is created also create a new cart
        new_cart = Cart(user=myuser,cart='{}')
        new_cart.save()

        messages.success(request,'Your account has been successfully created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        return HttpResponse("404 - NOT FOUND")

def handleLogin(request):
    if request.method == "POST":
        #get the post parameters
        loginemail = request.POST['loginEmail']
        loginpass = request.POST['loginPassword']
        user = authenticate(email=loginemail,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            if user.is_nurseryManager:
                return redirect('/nursery')
            else:
                return redirect('/shop')
        else:
            messages.error(request,'Invalid credentials, Please try again')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return HttpResponse('404 - Error Found')

def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully logged out')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

