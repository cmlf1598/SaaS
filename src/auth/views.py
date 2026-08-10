from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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

# def register_view(request):
#     return render(request, "auth/login.html", {})
