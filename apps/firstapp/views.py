from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import re
import bcrypt
from .models import *

def homerender(request):

    return render(request, 'homerender.html')

def register(request):

    check = True

    password = request.POST['password']
    email = request.POST['email']
    print email

    if len(password) < 8:
        messages.add_message(request, messages.ERROR, 'invalid password')
        check = False

    if request.POST['confirm'] != request.POST['password']:
        messages.add_message(request, messages.ERROR, 'Passwords do not match')
        check = False

    if len(request.POST['first_name']) == 0:
        messages.add_message(request, messages.ERROR, 'First name cannot be blank')
        check = False

    if len(request.POST['alias']) == 0:
        messages.add_message(request, messages.ERROR, 'Alias cannot be blank')
        check = False

    if len(request.POST['bday']) == 0:
        messages.add_message(request, messages.ERROR, 'Birthday cannot be blank')
        check = False

    email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if not email_re.match(email):
        messages.add_message(request, messages.ERROR, 'Email is not valid')
        return redirect('/')
        check = False

    if check ==  True:

        try:

            print 'try is working'
            hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            first_name = request.POST['first_name']
            alias = request.POST['alias']
            email = request.POST['email']
            birthday = request.POST['bday']
            user = User.objects.create(name=first_name, alias=alias, password=hashed, email=email, birthday=birthday)
            request.session['first_name'] = user.name
            request.session['id'] = user.id
            request.session['email'] = user.email

            return redirect('/quotes')

        except:
            messages.add_message(request, messages.ERROR, 'Email already exists')
            return redirect('/')

    return redirect('/')

def login(request):

    try:
        user = User.objects.get(email=request.POST['email'])
        request.POST['email'] == 0
        if bcrypt.hashpw(request.POST['password'].encode(), user.password.encode()) == user.password:
            request.session['first_name'] = user.name
            request.session['id'] = user.id
            request.session['email'] = user.email
            return redirect('/quotes')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Password')
            return redirect('/')
    except:
        messages.add_message(request, messages.ERROR, 'Invalid Email')
        return redirect('/')

def quotes(request):


    user = User.objects.all()
    quotes = Quote.objects.all()

    favorites = Favorite.objects.all()


    context = {
    'user': user,
    'quotes': quotes,
    'favorites': favorites,
    }

    return render(request, 'quotes.html', context)

def addquotes(request):

    check = True

    quoteauthor = request.POST['first_name']
    print quoteauthor
    message = request.POST['message']
    print message

    if len(quoteauthor) < 3:
        messages.add_message(request, messages.ERROR, 'Your name requires more than 3 characters')
        check = False

    if len(message) < 10:
        messages.add_message(request, messages.ERROR, 'Your message requires more than 10 characters')
        check = False

    if check == True:
        Quote.objects.create(message=message, author=quoteauthor, user_id=request.session['id'])
        return redirect('/quotes')

    return redirect('/quotes')

def favquotes(request, id):

    qmessage = request.POST['qmessage']

    favorite = Favorite.objects.create(favorite=qmessage, user_id=id, quote_id=id)


    return redirect('/quotes')





def renderuserpage(request, id):

    user = User.objects.get(id=id)
    quote = Quote.objects.filter(user_id=id)
    quotenum = Quote.objects.filter(user_id=id).count()

    context = {
    'user': user,
    'quote': quote,
    'quotenum': quotenum
    }
    return render(request, 'userpage.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    return redirect('/quotes')
