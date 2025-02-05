import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from .models import Issue
from .form import CreateIssueForm, UpdateIssueForm
from users.models import User

@login_required(login_url='login')
def issue_details(request, pk):
    issue = Issue.objects.get(pk=pk)
    t = User.objects.get(username=issue.created_by.username)
    issues_per_user = t.created_by.all()
    context = {
        'issue': issue,
        'issues_per_user': issues_per_user
    }
    return render(request, 'issue/issue_details.html', context)


# create issue
@login_required(login_url='login')
def create_issue(request):
    if request.method == 'POST':
        form = CreateIssueForm(request.POST, request.FILES)  
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.save()

            # Send email notification to the admin
            send_mail(
                subject='New Issue Submitted',
                message=f'Hello Admin,\n\nA new issue has been submitted by {request.user.username}.\n\nTitle: {var.title}\n\nPlease review it.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['ahumuzacedric@gmail.com'],  
                fail_silently=False,
            )

            messages.success(request, 'Your issue has been successfully submitted.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please try again.')
            return redirect('create-issue')
    else:
        form = CreateIssueForm()
        context = {
            'form': form
        }
        return render(request, 'issue/create_issue.html', context)

    

@login_required(login_url='login')
def update_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    if not issue.is_resolved:
        if request.method == 'POST':
            form = UpdateIssueForm(request.POST, request.FILES, instance=issue)  
            if form.is_valid():
                form.save()
                messages.success(request, 'Your issue has been updated.')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong. Please try again')
                return redirect('update-issue', pk=pk)
        else:
            form = UpdateIssueForm(instance=issue)
            context = {
                'form': form
            }
            return render(request, 'issue/update_issue.html', context)
    else:
        messages.warning(request, 'You cannot update a resolved issue.')
        return redirect('dashboard')

@login_required(login_url='login')
def all_issues(request):
    issues = Issue.objects.filter(created_by=request.user)
    context = {
        'issues': issues
    }
    return render(request, 'issue/all_issues.html', context)

# view issue queue
@login_required(login_url='login')
def issue_queue(request):
    issues = Issue.objects.filter(issue_status='Pending')
    context = {
        'issues': issues
    }
    return render(request, 'issue/issue_queue.html', context)

# accept a issue from the queue
@login_required(login_url='login')
def accept_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.assigned_to = request.user
    issue.issue_status = 'Active'
    issue.accepted_date = datetime.datetime.now()
    issue.save()

    # Send email to the issue creator
    send_mail(
        subject='Your Issue Has Been Accepted',
        message=f'Hello {issue.created_by.username},\n\nYour issue titled "{issue.title}" has been accepted by {request.user.username} and is now being worked on.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[issue.created_by.email],  
        fail_silently=False,
    )

    messages.info(request, 'Issue has been accepted.')
    return redirect('workspace')

# close a issue
@login_required(login_url='login')
def close_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    issue.issue_status = 'Completed'
    issue.is_resolved = True
    issue.closed_date = datetime.datetime.now()
    issue.save()

    # Send email notification to the issue creator
    send_mail(
        subject='Your Issue Has Been Resolved',
        message=f'Hello {issue.created_by.username},\n\nYour issue titled "{issue.title}" has been resolved.\n\nThank you for your patience.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[issue.created_by.email],  
        fail_silently=False,
    )

    messages.info(request, 'Issue successfully resolved!')
    return redirect('issue-queue')

# issue admin is working on
@login_required(login_url='login')
def workspace(request):
    issue = Issue.objects.filter(assigned_to=request.user, is_resolved=False)
    context = {
        'issue': issue
    }
    return render(request, 'issue/workspace.html', context)

# all closed/resolved issues
@login_required(login_url='login')
def all_issues_resolved(request):
    issue = Issue.objects.filter(assigned_to=request.user, is_resolved=True)
    context = {
        'issue': issue
    }
    return render(request, 'issue/all_issues_resolved.html', context)

@login_required(login_url='login')
def real_time_issue_data(request):
    if request.user.is_student:
        data = {
            'in_progress_count': Issue.objects.filter(created_by=request.user, issue_status='Active').count(),
            'pending_count': Issue.objects.filter(created_by=request.user, issue_status='Pending').count(),
            'completed_count': Issue.objects.filter(created_by=request.user, is_resolved=True).count(),
        }
    elif request.user.is_admin:
        data = {
            'open_count': Issue.objects.filter(issue_status='Pending').count(),
            'in_progress_count': Issue.objects.filter(issue_status='Active').count(),
            'resolved_count': Issue.objects.filter(is_resolved=True).count(),
        }
    else:
        data = {}

    return JsonResponse(data)

@login_required(login_url='login')
def issue_queue(request):
    issues = Issue.objects.filter(issue_status='Pending')
    paginator = Paginator(issues, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'issues': page_obj,
    }
    return render(request, 'issue/issue_queue.html', context)