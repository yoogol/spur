from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from todoapp.models import Task, Project, Goal
from django.urls import reverse, reverse_lazy

@csrf_exempt
def manage_goal(request):
    if request.method == 'GET':
        goal_id = request.GET.get('goal_id')
        print("get me an goal with id ", goal_id )
    if request.method == 'POST':
        print("create a new goal")
    if request.method == 'PUT':
        goal_id = request.PUT.get('goal_id')
        print("edit goal with id ", goal_id)
    if request.method == 'DELETE':
        goal_id = request.DELETE.get('goal_id')
        print("delete goal with id ", goal_id)
    return True


@csrf_exempt
def manage_project(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id')
        print("get me an project with id ", project_id )
    if request.method == 'POST':
        goal_id = request.POST.get('goal_id')
        print("create a new project under goal ", goal_id)
    if request.method == 'PUT':
        project_id = request.PUT.get('project_id')
        print("edit project with id ", project_id)
    if request.method == 'DELETE':
        project_id = request.DELETE.get('project_id')
        print("delete project with id ", project_id)
    return True


@csrf_exempt
def manage_task(request):
    response_data = {}
    try:
        task_id = request.GET.get('task_id')
        task = Task.objects.get(id=task_id)
        project_id = request.GET.get('project_id')
        if request.GET.get('type') == 'change_status':
            task.status = request.GET.get('status')
            task.save()
        response_data = {
            'status': 'ok',
            'redirect_url': reverse_lazy('todoapp:show_projects_for_goal', kwargs={'goal_id': task.project.goal_id},
                                current_app='todoapp')
        }
    except:
        response_data = {
            'status': 'error'
        }
    return JsonResponse(response_data)