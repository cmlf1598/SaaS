from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == "POST":
        # grab credentials
        username = request.POST.get("username") or None
        password = request.POST.get("password") or None
        if all([username, password]):
            user = authenticate(request, username=username, password=password)  # verify credentials against database. Login if all ok.
            if user is not None:
                login(request, user)  # from false to true
                return redirect("/")
            # invalid credentials — you may want to show an error here
            return render(request, "auth/login.html", {"error": "Invalid username or password"})
    
    # GET request — just show the empty login form
    return render(request, "auth/login.html", {})

def register_view(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username") or None
        email = request.POST.get("email") or None
        password = request.POST.get("password") or None
        # query for the db of the username and email
        # username_exists = User.objects.filter(username__iexact=username).exists()
        # email_exists = User.objects.filter(email__iexact=username).exists()
        try:
            User.objects.create_user(username, email=email, password=password)
        except:
            pass
    return render(request, "auth/register.html", {})
