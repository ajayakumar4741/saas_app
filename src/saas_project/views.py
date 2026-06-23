import pathlib
from django.http import HttpResponse
from django.shortcuts import redirect, render
from visits.models import PageVisit
from django.contrib.auth import authenticate, login


current_file_path = pathlib.Path(__file__).resolve().parent
def home(request, *args, **kwargs):
    print('Current file path:', current_file_path)
    if request.user.is_authenticated:
        print(request.user.first_name)
    # Create a new PageVisit instance once
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    my_content = {
        'title': 'My Home Page',
        'page_visits': page_qs.count(),
        'percentage': (page_qs.count() * 100.0/ qs.count()) if qs.count() > 0 else 0,
        'total_visits': qs.count(),
        
    }
    html_template = 'home.html'
    PageVisit.objects.create(path=request.path)
    # html_file_path = current_file_path / 'home.html'
    # html_ = html_file_path.read_text()
    
    # Return the content as an HTTP response
    return render(request, html_template, my_content)

def login_user(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('/')  # Replace 'home' with the name of your home view
    else:
        # Return an 'invalid login' error message.
        return render(request, 'login.html', {"message": "Invalid username or password."})