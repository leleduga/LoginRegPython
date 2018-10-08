
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from . models import *
import bcrypt

def index(request):
    if "errors" in request.session:
        errors=request.session["errors"]
        del request.session["errors"]
    else:
        errors=[]    
    context={
        "errors":errors
    }
    return render(request, 'loginreg/index.html', context)

def create(request):
    data_is_valid, errors = User.objects.basic_validator(request.POST)
    print ('data is valid',data_is_valid)
    print (errors)
    if  data_is_valid:    
        loginreg= User.objects.create(
            firstname=request.POST["firstname"],
            lastname=request.POST["lastname"],
            email=request.POST["email"],
            password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()),
        )
        request.session['firstname'] = request.POST['firstname']
        request.session['lastname']=request.POST['lastname']
        request.session['email']=request.POST['email']
    
        return redirect('/success')
    else:
        request.session["errors"]=errors
        return redirect('/') 
    # if User.objects.filter(email=request.POST['email']).count()>0:
    #     request.session["errors"]=errors
    #     print("Duplicate Email")   
    #     return redirect('/')   
    # else:
    #     redirect('/success')     

def success(request):
    user = User.objects.get(email=request.session["email"])
    print(user.email)
    context = {
        "user":user
    }
    return render(request, 'loginreg/success.html', context)


def validate_login(request):
    user = User.objects.get(email=request.POST['email'])
    print(user.email)
    print(user.password)
    print (user.password.encode())

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['email'] = request.POST['email']
        request.session['firstname']=user.firstname
        print("password match")
        return redirect('/success')
    else:
        request.session["errors"]=errors
        print("failed password") 
        return redirect('/')  
       





