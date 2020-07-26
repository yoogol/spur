from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Goal, Task, Project
from django.contrib.auth import login, authenticate, logout
from todoapp.forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from todoapp.tokens import account_activation_token, generate_invite_token
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse
import json
import datetime
import sendgrid
from sendgrid.helpers.mail import *
import os
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy, reverse
from .calculations import calculate_todays_tasks

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import Task as TaskForm
from .forms import Project as ProjectForm


sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
from_email = Email("yulia@yuliashea.com")


# Create your views here.
@login_required
def my_goals(request):
    goals = Goal.objects.filter(owner=request.user).order_by('order_number')
    return render(request, 'todoapp/goals.html', {'goals': goals})
    # return render(request, 'todoapp/goals.html')


def show_todays_tasks(request):
    today_data = calculate_todays_tasks()
    return render(request, 'todoapp/tasks_for_today.html', {'today_data': today_data})


def show_projects_for_goal(request, goal_id):
    projects_data = []
    goal = Goal.objects.get(id=goal_id)
    goal_projects = goal.goal_projects.filter(status="A").order_by('-goal_kudos')
    for project in goal_projects:
        project_data = {
            'project': project,
            'tasks': project.project_tasks.all().order_by('order_within_project')
        }
        projects_data.append(project_data)

    return render(request, 'todoapp/projects.html', {'goal': goal, 'projects_data': projects_data})


def edit_task(request, project_id=None, task_id=None):
    if request.method == 'GET':
        if not task_id:
            task_form = TaskForm()
        else:
            task = Task.objects.get(id=task_id)
            task_form = TaskForm(instance=task)

    elif request.method == 'POST':
        if not task_id:
            task = Task(project_id=project_id)
        else:
            task = Task.objects.get(id=task_id)
        task_form = TaskForm(request.POST,instance=task)
        if task_form.is_valid():
            new_task = task_form.save()
            new_task.rearrange_tasks_order()
            return HttpResponseRedirect(reverse_lazy('todoapp:show_projects_for_goal', kwargs={'goal_id': task.project.goal_id},
                                current_app='todoapp'))
    return render(request, 'todoapp/task.html', {'form': task_form, 'project_id': project_id, 'task_id': task_id})


def edit_project(request, goal_id=None, project_id=None):
    if request.method == 'GET':
        if not project_id:
            project_form = ProjectForm()
        else:
            project = Project.objects.get(id=project_id)
            project_form = ProjectForm(instance=project)

    elif request.method == 'POST':
        if not project_id:
            project = Project(goal_id=goal_id)
        else:
            project = Project.objects.get(id=project_id)
        project_form = ProjectForm(request.POST,instance=project)
        if project_form.is_valid():
            new_project = project_form.save()
            return HttpResponseRedirect(reverse_lazy('todoapp:show_projects_for_goal', kwargs={'goal_id': project.goal_id},
                                                     current_app='todoapp'))
    return render(request, 'todoapp/edit_project.html', {'form': project_form, 'goal_id': goal_id, 'project_id': project_id})

def signup(request, token=None):
    logout(request)
    my_email = None
    if token == "None":
        token = None
    if token:
        print("token")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            username = form.cleaned_data.get('username').strip()
            user.email = username.strip()
            user.save()
            current_site = get_current_site(request)
            user_verified = False

            if not user_verified:
                subject = 'Activate Your Spur Account'
                text = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = To(username)
                content = Content("text/plain", text)
                mail = Mail(from_email=from_email, subject=subject, to_emails=to_email, html_content=content)
                response = sg.client.mail.send.post(mail.get())
                return redirect('account_activation_sent')
            else:
                login(request, user)
                return redirect('giftsharingapp:my-gifts')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'my_email': my_email, 'token': token})


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.userinfo.email_confirmed = True
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('todoapp:my-goals')
        else:
            # invalid link
            return render(request, 'registration/account_activation_invalid.html')

@csrf_exempt
def accept_invite(request, token=None):
    if token:
        return HttpResponseRedirect(reverse('signup', args=(token,)))
    else:
        invite_id = request.POST.get('invite_id')
        invite = FriendInvite.objects.get(id=invite_id)
    if request.user.id != invite.sent_to_user_id:
        return HttpResponse(
            json.dumps({'result': 'Error'}),
            content_type='application/json'
        )
    success, message = invite.accept_invite()
    response_data = {}
    response_data['redirect_url'] = reverse('giftsharingapp:friends-gifts')
    response_data['message'] = message
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

