import pathlib
from django.http import HttpResponse
from django.shortcuts import redirect, render
from visits.models import PageVisit
from django.contrib.auth import authenticate, login, get_user_model
from django.db.models import Q

User = get_user_model()

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
    if request.method != "POST":
        return render(request, 'login.html')

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return render(request, 'login.html', {"message": "Username and password are required."})

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('/')  # Replace 'home' with the name of your home view
    else:
        # Return an 'invalid login' error message.
        return render(request, 'login.html', {"message": "Invalid username or password."})
    
def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not email or not password:
            return render(request, 'reg.html', {"message": "All fields are required."})

        # Check if the username and email already exists
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            return render(request, 'reg.html', {"message": "Username or email already exists."})

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Redirect to login page after successful registration
        return redirect('/login/')  # Replace with your login URL

    return render(request, 'reg.html')
