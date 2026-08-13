import pathlib
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from django.http import HttpResponse

this_dir = pathlib.Path(__file__).resolve().parent # parent directory

from visits.models import PageVisit

LOGIN_URL = settings.LOGIN_URL

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.first_name)
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all() # get all
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0
    my_title = "My page"
    html_template = "home.html" #path inside settings.py
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(), # count all rows of database (page visits)
        "percent": percent,
        "total_visit_count": qs.count(),
    } # passed to home.html in {{}}
    html_ = ""
    PageVisit.objects.create(path=request.path) # for visits counter to this specific page 
    return render(request, html_template, my_context) 

# Returns HTML code
# args and kwargs in case there are any other arguments
def my_old_home_page_view(request, *args, **kwargs):
    my_title = "My page"
    my_context = {
        "page_title": my_title
    }
    
    html_ = """
    <!DOCTYPE html>
    <html>

    <body>
        <h1>{page_title} anything?</h1>
    </body>
    </html>
    """.format(**my_context) #page_title=my_title
    # html_file_path = this_dir / "home.html"
    # html_ = html_file_path.read_text()
    return HttpResponse(html_)

VALID_CODE = "abc123"

def pw_protected_view(request, *args, **kwargs):
    # once the valid code is input and you have logged in as a user, no need to input the code again. 
    # until signing out. 
    is_allowed = request.session.get('protected_page_allowed') or 0
    # print(request.session.get('protected_page_allowed'), type(request.session.get('protected_page_allowed')))
    if request.method == "POST":
        user_pw_sent = request.POST.get("code") or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})

#authentication only (logged in or not)
@login_required(login_url=LOGIN_URL)
def user_only_view(request, *args, **kwargs):
    #print(request.user.is_staff)
    return render(request, "protected/user-only.html")

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html")
