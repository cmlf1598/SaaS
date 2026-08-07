import pathlib
from django.shortcuts import render
from django.http import HttpResponse

this_dir = pathlib.Path(__file__).resolve().parent # parent directory

from visits.models import PageVisit

def home_page_view(request, *args, **kwargs):
    qs = PageVisit.objects.all() # get all
    page_qs = PageVisit.objects.filter(path=request.path)
    my_title = "My page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(), # count all rows of database (page visits)
        "percent": (page_qs.count() * 100.0) / qs.count(),
        "total_visit_count": qs.count(),
    } # passed to home.html in {{}}
    html_ = ""
    html_template = "home.html" #path inside settings.py
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

