from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterStudentForm


def register_student(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_student = True
            var.save()
            messages.success(request, 'Your account has been Successfully created. Please login to continue')
            return redirect('login')
        else:
            messages.warning(request, "Something went wrong, Please Try again")
            return redirect('register-student')
    else:
        form = RegisterStudentForm()
        context = {
            'form': form
            }
        return render(request, 'users/register_student.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Login Success')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please Try again')
            return redirect('login')
    else:
        return render(request, 'users/login.html')




def logout_user(request):
    logout(request)
    messages.success(request, 'Please login to continue')
    return redirect('login')
