from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.db.models import Q
import datetime, sys

from django.contrib.auth.models import User
from .models import Category, Post, Reply
#from .models import User

def index(request):
    if request.method == "GET":
        context = {}
        # Get all public categories.
        public_cats = Category.objects.filter(private=False)
        context["public_cats"] = public_cats
        # Add the count of each post to the category object so we can list it
        # in the UI.
        for cat in public_cats:
            cat.pub_count = Category.objects.post_count(cat.id)

        # Get all private categories if the user is authenticated..
        if request.user.is_authenticated:
            private_cats = Category.objects.filter(private=True)
            context["private_cats"] = private_cats
            # Add the count of each post to the category object so we can list
            # it in the UI.
            for cat in private_cats:
                cat.pri_count = Category.objects.post_count(cat.id)

        return render(request, 'forum/index.html', context)
    else:
        messages.error(request, "Not allowed")
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
            messages.success(request, "Welcome")
            return redirect(reverse('forum:index'))
        else:
            messages.error(request, "Login errors")
            return redirect(reverse('forum:index'))
    else:
        messages.error(request, "Please login first.")
        return redirect(reverse('forum:index'))


def categories(request, category_id=0):
    """
    Function to create new categories.
    """
    if request.method == "GET":
        if category_id is 0:
            print("getting cats")
            context = {"cats": Category.objects.all()}
            return render(request, "forum/categories.html", context)
        elif category_id > 0:
            #post = Post.objects.get(category__pk=category_id)
            post = Post.objects.filter(category__id=category_id)
            context = {
                    "post": post,
                    "cat": Category.objects.get(id=category_id)
                    }
            #print(context)
            return render(request, "forum/category.html", context)


    if request.method == "POST":
        print("POST!")
        #print(request.POST["name"])
        #print(request.user)
        print(request.POST)
        print(request.POST["private"])
        cat = Category.objects.filter(name=request.POST["name"])
        #print(cat.count())
        if cat.count() is 0:
            create_return = Category(name=request.POST["name"]
                    , private=request.POST["private"]
                    , created_by=request.user)
            create_return.save()
            messages.error(request, "Category Created")
            return redirect(reverse('forum:index'))
        else:
            messages.error(request, "Category Exists Already")
            return redirect(reverse("forum:categories"))

    else:
        messages.error(request, "Not allowed")
        return redirect(reverse('forum:index'))

def post(request, category_id=0, post_id=0):
    if request.method == "GET":
        print("GET")
        print(category_id)
        print(post_id)
        #context = {"category_id": category_id}
        context = {
                "category_id": category_id,
                "post": Post.objects.get(pk=post_id),
                "replies": Reply.objects.filter(post__pk=post_id)
                }
        return render(request, "forum/post.html", context)
    elif request.method == "POST":
        #print("POST")
        owner = request.user
        category = Category.objects.get(pk=category_id)
        title = request.POST["title"]
        body = request.POST["body"]
        new_post = Post(owner=owner, category=category, title=title, body=body)
        new_post.save()
        messages.success(request, "Posted")
        return redirect(reverse('forum:categories', args=[category_id]))

    else:
        messages.error(request, "Not allowed")
        return redirect(reverse('forum:index'))


def reply(request, category_id=0, post_id=0):
    if request.method == "GET":
        messages.error(request, "Not allowed")
        context = {
                "category_id": category_id,
                "post": Post.objects.get(pk=post_id)
                }
        return render(request, "forum/post.html", context)
    elif request.method == "POST":
        print("POST")
        owner = request.user
        post = Post.objects.get(pk=post_id)
        body = request.POST["body"]
        new_reply = Reply(owner=owner, post=post, body=body)
        new_reply.save()
        messages.success(request, "Posted")
        return redirect(reverse('forum:post', args=[category_id, post_id]))

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
