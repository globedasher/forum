from django.test import TestCase, Client

from . import views
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Organization

# Create your tests here.

class MyTestCase(TestCase):

    def setUp(self):
        # Create one test user
        user = User.objects.create_user(
                   "testname",
                   "test@email.com",
                   "Password1!",
               )
        #user.save()
        org = Organization(name="Junebug", employee=user)
        org.save()
        # Create another test user
        user = User.objects.create_user(
                   "firefly",
                   "firefly@mailcatch.com",
                   "Generic1",
               )
        user.first_name = "Joss"
        user.last_name = "Whedon"
        #user.save()
        org = Organization(name="Junebug", employee=user)
        org.save()


    def user_org_lookup(self, name):
        user = User.objects.filter(username=name)
        org = Organization.objects.filter(name="Junebug")
        #print(user[0])
        self.assertEqual(user[0].username, name)
        #print(org[0].name)
        self.assertEqual(org[0].name, "Junebug")


    def test_testname_org_lookup(self):
        self.user_org_lookup("testname")

    def test_firefly_org_lookup(self):
        self.user_org_lookup("firefly")

    def test_temple_org_lookup(self):
        try:
            self.user_org_lookup("temple")
        except:
            print("No user with that name.")

    def test_root_url(self):
        c = Client()
        res = c.get('/')
        print(res.status_code)
        #print(res.content)
        self.assertEqual(res.status_code, 200)
