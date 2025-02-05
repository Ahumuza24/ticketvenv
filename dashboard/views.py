from django.shortcuts import render, redirect

from issue.models import Issue


# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
