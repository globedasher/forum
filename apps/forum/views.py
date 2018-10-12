from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.db.models import Q
import datetime

from django.contrib.auth.models import User

#from .models import User

def index(request):
    # If the user is already authenticated, return them to the home page
    if request.user.is_authenticated:
        return redirect(reverse('auth:home'))
    try:
        all_users = User.objects.all()
        context = { 'all_users': all_users }
        return render(request, 'forum/index.html', context)
    except:
        return render(request, 'forum/index.html')

def home(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login first.")
        return redirect(reverse('auth:index'))
    if request.user.is_superuser:
        pass
        #print("is superuser")
    else:
        #print("is superuser")
        print(request.user.email)
        user = User.objects.get(pk=request.user.pk)
        print("home else")
        print(orgs)
        for org in orgs:
            print("org in orgs")
            print(org.name)
    context = {'orgs': orgs}
    return render(request, "forum/home.html", context)

def users(request):
    #print(request)
    if not request.user.is_authenticated:
        messages.error(request, "Please login first.")
        return redirect(reverse('auth:index'))
    all_users = User.objects.all()
    context = { 'all_users': all_users }
    return render(request, "forum/users.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome")
            return redirect(reverse('auth:home'))
        else:
            messages.error(request, "Login errors")
            return redirect(reverse('auth:index'))
    else:
        messages.error(request, "Please login first.")
        return redirect(reverse('auth:index'))



def logout_view(request):
    #del request.session['id']
    #del request.session['email']
    logout(request)
    return redirect(reverse('auth:index'))



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

        mail_result = send_mail(subject = "Invitation from: " + user.email # Subject
                               , message = "Email"
                               , from_email = "fm65cq@gmail.com" # From
                               , recipient_list = ["globe.dasher@gmail.com"] # To
                               , fail_silently=False
                               , html_message=body # Message body
                               )
        #login(request, user)
        #print(mail_result)
        if mail_result > 0:
            messages.success(request, "Email sent to " + request.POST['email'].lower())
        else:
            messages.success(request, "Email sent to " + request.POST['email'].lower())
            messages.success(request, "Only " + mail_result + " sent")

        return redirect(reverse('auth:index'))
    else:
        messages.error(request, "Incorrect Http request.")
        return redirect(reverse('auth:index'))


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
        return redirect(reverse('auth:home'))
    else:
        messages.error(request, "Incorrect Http request.")
        return redirect(reverse('auth:index'))

def mail_queue(request):
    #print("Queue Request")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    rc = socket.connect("ipc:///tmp/mail_queue_ipc")
    #print(request.method)
    if request.method == "GET":
        socket.send(b"read_queue")
        mail_queue = socket.recv()
        mail_queue = eval(mail_queue)
        #print(mail_queue)
        context = {
                "mail_queue": mail_queue
                }
        return render(request, 'forum/queue.html', context)
    elif request.method == "POST":
        if not request.POST["ident"]:
            messages.error(request, "Select an ident")
            socket.send(b"read_queue")
            mail_queue = socket.recv()
            mail_queue = eval(mail_queue)
            context = { "mail_queue": mail_queue }
            return render(request, 'forum/queue.html', context)
        command = "create: %s" % (request.POST["ident"])
        socket.send(str.encode(command))
        service_response = socket.recv()
        service_response = eval(service_response)

        # After we send the node to the mail_queue, get the queue to display
        # again.
        socket.send(b"read_queue")
        mail_queue = socket.recv()
        mail_queue = eval(mail_queue)
        #print(mail_queue)
        context = {
                "mail_queue": mail_queue
                }
        return render(request, 'forum/queue.html', context)
