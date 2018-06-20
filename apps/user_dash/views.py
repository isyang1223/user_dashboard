from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
# Create your views here.
def index(request):
    

    return render(request, "user_dash/index.html")
    
def signin(request):
    
    return render(request, "user_dash/signin.html")

def register(request):
    

    return render(request, "user_dash/register.html")


def reg(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)
    if 'id' not in errors:
        for tag, error in errors.iteritems():
            messages.error(request,error, extra_tags = tag)
        if 'reg' in request.POST:
            return redirect('/users/new')
        else:
            return redirect('/register')
    else:
        if 'reg' in request.POST:
            return redirect('/dashboard')
        else:
            request.session['logged_id'] = errors['id']
            request.session['user_level'] = errors['user_level']
            return redirect('/dashboard')
    return redirect('/register')

# def reg(request):
#     if request.method == 'POST':
#         errors = User.objects.registration_validator(request.POST)
#         if "user" in errors: 
        
#             request.session["user_level"] = errors["user"].user_level
#             request.session["user"] = errors["user"]
#             request.session["idk"] = "registered"
#             request.session["logged_id"] = errors["user"].id
#             request.session["logged_name"] = errors["user"].fname

#             return redirect('/users/new')
#         else:
#             for tag, error in errors.iteritems():
#                 messages.error(request, error, extra_tags=tag)
#             return redirect('/register')
#     else:
#         return redirect("/register")

def create(request):
    
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)

        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/new')
        else:
        
            return redirect("/dashboard")

def edit(request, id):
    if not "logged_id" in request.session:
        return redirect("/")

    key= User.objects.get(id=id)
    data={
            "this_user": key
    }
    
    if request.session["user_level"] == "normal":
        return render (request, "user_dash/normal_edit.html", data)
    else:
        return render (request, "user_dash/admins_edit.html", data)


def normal_edit(request, id):
    if not "logged_id" in request.session:
        return redirect("/")
    key= User.objects.get(id=id)
    data={
            "loggeduser": key
    }
    
    
    return render (request, "user_dash/normal_edit.html", data)

def edit_normalname(request, id):
    if not "logged_id" in request.session:
        return redirect("/")
    if request.method == 'POST':
        errors = User.objects.edit_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect("/users/edit/normal/"+str(id))
        else:
            
            return redirect("/dashboard")

    return redirect("/dashboard")

def edit_normalpassword(request, id):
    if request.method == 'POST':
        errors = User.objects.pw_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/edit/normal/'+str(id))
        else:
        
            return redirect("/dashboard")

    
def edit_info(request, id):
    
    if request.method == 'POST':
        print "this is ++++++++++++++++++++"
        errors = User.objects.edit_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/edit/'+str(id))
        else:
        
            return redirect("/dashboard")

    return redirect("/dashboard")



def edit_admin(request, id):
    if request.method == 'POST':
        print "sup vinny"
        errors = User.objects.edit_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        

    return redirect("/dashboard/admin")
   

def edit_password(request, id):
    if request.method == 'POST':
        errors = User.objects.pw_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/edit/'+str(id))
        else:
        
            return redirect("/dashboard")

    return redirect("/dashboard")

def edit_normaldescription(request, id):
    this_user = User.objects.filter(id= request.POST["this_user_id"])
    this_user.update(desc=request.POST["desc"])


    return redirect("/dashboard")

def wall(request, id):
    if request.method == 'POST':
        errors = User.objects.message_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/show/'+id)
        else:
        
            return redirect('/users/show/'+id)
    return redirect("/users/show/"+id)


def comment(request, id):
    if request.method == 'POST':
        errors = User.objects.comment_validator(request.POST)
        if errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/users/show/'+id)
        else:
        
            return redirect('/users/show/'+id)
    return redirect("/users/show/"+id)

def usershow(request, id):
    if not "logged_id" in request.session:
        return redirect("/")
    print"*********************** this is the id", id
    key= User.objects.get(id=id)
    key1=key.received_msgs.all()
    key2=Comment.objects.all()

    data={
            "loggeduser": key,
            "usersmessages": key1,
            "allcomments": key2,
    }
    print"*******************", data["usersmessages"]
    return render(request, "user_dash/users_show.html", data)

def remove(request, id):
    User.objects.get(id=id).delete()
   
    return redirect("/dashboard")

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if "user" in errors:
            request.session["user_level"] = errors["user"].user_level
            request.session["idk"] = "registered"
            request.session["logged_id"] = errors["user"].id
            request.session["logged_name"] = errors["user"].fname
            if errors["user"].user_level == "admin":
    
                return redirect("/dashboard/admin")
            else:
                return redirect('/dashboard')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/signin')
    else:
        return redirect("/signin")

def user_dashboard(request):
    if not "logged_id" in request.session:
        return redirect("/")
    else:
        data = {
            "user": User.objects.all()
        }
        if request.session["user_level"] == "normal":
            return render(request, "user_dash/user_dashboard.html", data)
        else:
            return render(request, "user_dash/admin_dashboard.html", data)

def usersnew(request):
    if not "logged_id" in request.session:
        return redirect("/")

    if request.session["user_level"] == "normal":
        return redirect("/dashboard")

    return render(request, "user_dash/users_new.html")

def admin_dashboard(request):
    if not "logged_id" in request.session:
        return redirect("/")
    else:
        data = {
            "user": User.objects.all()
        }
        
        if request.session["user_level"] == "normal":
            return render(request, "user_dash/user_dashboard.html", data)
        else:
            return render(request, "user_dash/admin_dashboard.html", data)

def logout(request):
    request.session.clear()
    return redirect("/")


    