from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *
from .forms import *
from apps.travels.models import *
from apps.users.models import *

# Create your views here.
def index(request):
    return render(request, "login/index.html")

def registration(request):
    if request.method == "POST":
        validation = User.objects.validator(request.POST)

        if len(validation) == 0:
            # hash password
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

            # create new user
            new_user = User.objects.create(first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        username=request.POST['username'],
                                        email=request.POST['email'],
                                        password=hash1.decode())
                                        # birthday=request.POST['birthday'])

            request.session['id'] = new_user.id

            return redirect("/travels")
        else:
            for key, val in validation.items():
                messages.add_message(request,
                            messages.ERROR,
                            val,
                            key)
            return redirect("/")
    else:
        return redirect("/")

def login(request):
    # check if user exists
    results = User.objects.filter(email=request.POST['email_address'])
    if len(results) > 0:
        if bcrypt.checkpw(request.POST['pwd'].encode(), results[0].password.encode()):
            request.session['id'] = results[0].id
            return redirect("/travels")

    messages.add_message(request,
            messages.ERROR,
            "Email and/or password is invalid",
            "login")
    return redirect("/")

def logout(request):
    if 'id' in request.session:
        del request.session['id']
    return redirect("/")

