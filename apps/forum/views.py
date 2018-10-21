from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.db.models import Q
import datetime

from django.contrib.auth.models import User
from .models import Category, Post

#from .models import User

def index(request):
    # If the user is already authenticated, return them to the home page
    # NOTE: commented out to make a single page app.
    #if request.user.is_authenticated:
        #return redirect(reverse('forum:index'))
    try:
        all_users = User.objects.all()
        cats = Category.objects.all()
        context = {
                'all_users': all_users
                ,'cats': cats
                }
        return render(request, 'forum/index.html', context)
    except:
        return render(request, 'forum/index.html')

def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first.")
        return redirect(reverse('forum:index'))
    if request.user.is_superuser:
        pass
        #print("is superuser")
    else:
        #print("is superuser")
        print(request.user.email)
        user = User.objects.get(pk=request.user.pk)
        print("home else")

    posts = Post.objects.all()
    print(posts)
    for post in posts:
        print("post in posts")
        print(post.name)
    context = {'posts': posts}
    return render(request, "forum/home.html", context)

def users(request):
    #print(request)
    if not request.user.is_authenticated:
        messages.error(request, "Please login first.")
        return redirect(reverse('forum:index'))
    all_users = User.objects.all()
    context = { 'all_users': all_users }
    return render(request, "forum/users.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        #print(username)
        password = request.POST['password']
        #print(password)
        user = authenticate(request, username=username, password=password)
        #print(user)
        if user is not None:
            login(request, user)
            #messages.success(request, "Welcome")
            return redirect(reverse('forum:index'))
        else:
            messages.error(request, "Login errors")
            return redirect(reverse('forum:index'))
    else:
        messages.error(request, "Please login first.")
        return redirect(reverse('forum:index'))


def categories(request):
    """
    Function to create new categories.
    """
    if request.method == "GET":
        cats = Category.objects.all()
        print("cats.count")
        print(cats.count())
        #print("cats.count")
        context = {
                "categories": cats
                }
        #print(context)
        return render(request, "forum/categories.html", context)

    if request.method == "POST":
        print("POST!")
        #print(request.POST["name"])
        print(request.user)
        tuple_return = Category.objects.register(request.POST, request.user)
        if tuple_return[0] == False:
            messages.error(request, "Category Exists Already")
            return redirect(reverse("forum:categories"))
        elif tuple_return[0] == True:
            messages.error(request, "Category Created")
            return redirect(reverse('forum:index'))
    else:
        messages.error(request, "Not allowed")
        return redirect(reverse('forum:index'))




def logout_view(request):
    #del request.session['id']
    #del request.session['email']
    logout(request)
    return redirect(reverse('forum:index'))



#TODO: I need to build invite validation of form data...
def register(request):
    if request.method == "GET":
        return render(request, 'forum/register.html')
    elif request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'].lower())
        except:
            user = User.objects.create_user(
                    username=request.POST['email'].lower()
                    , email=request.POST['email'].lower()
                )

        #TODO: Determine if we should create an invitation table...
        user.save()

        body = ""

        with open("apps/forum/templates/email/email.html") as f:
            try:
                body += f.read()
            finally:
                f.close()

        print(body)

        subject = "Invitation from: " + user.email # Subject
        message = "Email"
        from_email = "fm65cq@gmail.com" # From
        recipient_list = ["globe.dasher@gmail.com"] # To

        mail_result = send_mail(subject
                               ,message
                               ,from_email
                               ,recipient_list
                               ,html_message=body
                               ,fail_silently=False
                               )
        #login(request, user)
        #print(mail_result)
        if mail_result > 0:
            messages.success(request, "Email sent to " + request.POST['email'].lower())
        else:
            messages.success(request, "Email sent to " + request.POST['email'].lower())
            messages.success(request, "Only " + mail_result + " sent")

        return redirect(reverse('forum:index'))
    else:
        messages.error(request, "Incorrect Http request.")
        return redirect(reverse('forum:index'))


#TODO: I need to build invite validation of form data...
def invite(request):
    if request.method == "GET":
        return render(request, 'forum/invite.html')
    elif request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'].lower())
        except:
            user = User.objects.create_user(
                    username=request.POST['email'].lower()
                    , email=request.POST['email'].lower()
                    , first_name = request.POST['first_name']
                    , last_name = request.POST['last_name']
                )
        user.save()
        value = auth_views.password_reset(request)

        #login(request, user)
        messages.success(request, "Successful invite!")
        return redirect(reverse('forum:home'))
    else:
        messages.error(request, "Incorrect Http request.")
        return redirect(reverse('forum:index'))
