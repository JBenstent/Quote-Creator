from django.shortcuts import render, redirect
from django.contrib import messages
import re
import bcrypt
from .models import *

def homerender(request):

    return render(request, 'homerender.html')

def register(request):

    check = True

    password = request.POST['password']

    if len(password) < 8:
        messages.add_message(request, messages.ERROR, 'invalid password')
        check = False

    if request.POST['confirm'] != request.POST['password']:
        messages.add_message(request, messages.ERROR, 'Passwords do not match')
        check = False

    if len(request.POST['first_name']) == 0:
        messages.add_message(request, messages.ERROR, 'First name cannot be blank')
        check = False

    if len(request.POST['last_name']) == 0:
        messages.add_message(request, messages.ERROR, 'Last name cannot be blank')
        check = False

    email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not email_re.match(request.POST['email']):
        messages.add_message(request, messages.ERROR, 'Email is not valid')
        check = False
        print 'email not valid'

    if check ==  True:
        try:
            hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            user = User.objects.create(name=first_name, last_name=last_name, email=email, password=hashed)

            request.session['first_name'] = user.name

            request.session['id'] = user.id
            request.session['email'] = user.email

            return redirect('/bookapphome')

        except:
            messages.add_message(request, messages.ERROR, 'Email already exists')
            return redirect('/')

    return redirect('/')

def login(request):

    try:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.hashpw(request.POST['password'].encode(), user.password.encode()) == user.password:
            request.session['first_name'] = user.name
            request.session['id'] = user.id
            request.session['email'] = user.email
            return redirect('/bookapphome')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Password')

    except:
        messages.add_message(request, messages.ERROR, 'Invalid Email')
