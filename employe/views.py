from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Emp, Userlogin, Contactus
from .form import ContactForm
from django.core.exceptions import PermissionDenied
from django.contrib import messages
import re
from django.db.models import Q 


# Index page view

def index(request):

    isActive = True
    if request.method == 'POST':
        check = request.POST.get("check")
        print(check)
        if check is None:
            isActive = False
        else:
            isActive = True
    return render(request, "index.html", {})

# About page view


def about(request):
    return render(request, "about.html", {})


def main(request):
    return render(request, "employe/main.html", {'isLogin': True})


# employee home page view
def employe_home(request):

    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        return redirect("/login/")

    user = Userlogin.objects.get(id=userId)
    if user.islogin is False:
        return redirect("/login/")

    emps = Emp.objects.all()
    return render(request, "employe/home_emp.html", {
        'emps': emps,
        'isLogin': True
    })


def add_employe(request):
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        return redirect("/login/")

    user = Userlogin.objects.get(id=userId)
    if user.islogin is False:
        return redirect("/login/")

    if request.method == "POST":
        # Data Fetch
        employee_name = request.POST.get("employee_name")
        employee_id = request.POST.get("employee_id")
        employee_phone = request.POST.get("employee_phone")
        employee_address = request.POST.get("employee_address")
        employee_working = request.POST.get("employee_working")
        employee_department = request.POST.get("employee_department")

        # Phone number validation
        if not re.match(r'^\+?1?\d{9,15}$', employee_phone):
            messages.error(
                request, 'Please enter a valid digit in the phone field.')
            return redirect("/employe/add_employe/")

        # Create model object and set data
        e = Emp()
        e.name = employee_name
        e.emp_id = employee_id
        e.phone = employee_phone
        e.address = employee_address
        e.department = employee_department
        if employee_working is None:
            e.working = False
        else:
            e.working = True

        # Save the object
        e.save()

        # Prepare msg
        messages.success(request, 'You have added new employee successfully')
        return redirect("/employe/home/")
    return render(request, "employe/add_employe.html", {'isLogin': True})

# Delete employe view


def delete_employe(request, employe_id):
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        return redirect("/login/")

    user = Userlogin.objects.get(id=userId)
    if user.islogin is False:
        return redirect("/login/")

    employe = Emp.objects.get(id=employe_id)
    employe.delete()
    messages.warning(request, 'Successfully deleted an employee details')

    return redirect("/employe/home/")

# Update employe view


def update_employe(request, employe_id):

    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        return redirect("/login/")

    user = Userlogin.objects.get(id=userId)
    if user.islogin is False:
        return redirect("/login/")

    employe = Emp.objects.get(pk=employe_id)
    return render(request, "employe/update_employe.html", {
        'employe':employe, 'isLogin': True
    })

# Data Fetch for update employee


def do_update_emp(request, employe_id):

    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        return redirect("/login/")

    user = Userlogin.objects.get(id=userId)
    if user.islogin is False:
        return redirect("/login/")

    if request.method == 'POST':
        employee_name = request.POST.get("employee_name")
        employee_id_temp = request.POST.get("employee_id")
        employee_phone = request.POST.get("employee_phone")
        employee_address = request.POST.get("employee_address")
        employee_working = request.POST.get("employee_working")
        employee_department = request.POST.get("employee_department")
# Model object and set data for update
        e = Emp.objects.get(pk=employe_id)
        e.name = employee_name
        e.emp_id = employee_id_temp
        e.phone = employee_phone
        e.address = employee_address
        e.department = employee_department
        if employee_working is None:
            e.working = False
        else:
            e.working = True
        e.save()
        messages.success(request, 'Successfully Updated')
    return redirect("/employe/home/")

# Contact view


def contact(request):

    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        return redirect("/login/")

    user = Userlogin.objects.get(id=userId)
    if user.islogin is False:
        return redirect("/login/")

    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(name)
        contact = Contactus()
        contact.name = name
        contact.email = email
        contact.message = message

        contact.save()
        messages.success(request, 'Thank you for contacting us!')
        return redirect("/employe/main/")

    else:
        form = ContactForm()
    return render(
        request, "employe/contact.html", {'form':form, 'isLogin': True})

# Login View


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        userQuerySet = Userlogin.objects.filter(username=username).filter(
            password=password)
        print(userQuerySet)
        if len(userQuerySet) > 0:
            for user in userQuerySet:
                user.islogin = True
                user.save()
                request.session['userId'] = user.id
                messages.success(request, 'You have logged in successfully')
            return redirect("/employe/main/")
        else:
            # Add an error message for unsuccessful login
            messages.error(request, 'Invalid username or password')
    return render(request, "auth/login.html", {'form':'helo'})

# User Registration


def registerUser(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        # Check if username or email already exists
        existing_user = Userlogin.objects.filter(Q(username=username) | Q(email=email)).first()

        if existing_user:
            # User with the same username or email already exists
            messages.error(request, 'Username or email already exists. Please use another.')
        else:
            user = Userlogin()
            user.username = username
            user.password = password
            user.email = email
            user.islogin = False

            # Save the object
            user.save()
            messages.success(request, 'Successfully registered, Please login now!')
            return redirect("/login/")

    return render(request, "auth/register.html", {'form': 'helo'})

# logout


def logoutUser(request):
    if 'userId' in request.session:
        userId = request.session['userId']
        user = Userlogin.objects.get(id=userId)
        user.islogin = False
        user.save()
        del request.session['userId']
        messages.warning(request, 'Logout Successful. See you next time!.')
    return redirect("/login/")

# Error handling


def handler404(request, exception):
    """Function to render the 404 page."""
    return render(request, '404.html', status=404)


def handler500(request):
    """ Function to render the 500 page."""
    return render(request, '500.html', status=500)


def handler403(request, exception):
    """Function to render the 403 page."""
    if isinstance(exception, PermissionDenied):
        return render(request, '403.html', status=403)
    else:
        # Handle unexpected errors with a generic 500 error page
        return render(request, '500.html', status=500)
