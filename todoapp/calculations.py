from django.utils import timezone

from .models import Project, Task
from django.db.models import Min


def calculate_todays_tasks():
    now = timezone.now()
    # get all active tasks
    # filter out those that follow a task that is not "not until"
    # get a score for each task depending on
    # is there a deadline?
    # - if yes,
    #   how close is it to deadline
    #   what's the task importance

    # - if not, how important is the task
    '''
    calculation
    
    1. get rid of anything not needed:
    - deleted
    - completed
    - not until tasks and the ones below them
    
    2. create top limit of tasks per project given the amount of time needed 
    total time of all tasks should not exceed 8 hours
    
    3. score tasks
    tasks with deadline
    - find all tasks above the one with deadline and assign importance accordingly
    - consider goal order and project kudos
    
    tasks without deadline
    - consider goal order and project kudos, also goal deadline/project deadline
    
    
    when a task is completed, cross it out. clear them only at the start of day
    '''

    projects = Project.objects.all()
    tasks = []
    not_until_tasks = Task.objects.filter(not_until__isnull=False, status='A')
    not_until_tasks_plus_ids = []
    for task in not_until_tasks:
        not_until_tasks_plus_ids.extend(Task.objects.filter(project=task.project, order_within_project__gte=task.order_within_project).values_list('id',flat=True))

    for project in projects:
        project_tasks = Task.objects.filter(project=project, status='A').order_by('order_within_project').exclude(id__in=not_until_tasks_plus_ids)
        if project_tasks.first():
            tasks.append(project_tasks.first())

    tasks = sorted(tasks, key=lambda t: t.score)

    # tasks = Task.objects.filter(status='A')
    # task_ids_to_exclude = []
    # for task in tasks:
    #     # exclude tasks with not_until and after
    #     if task.not_until and task.not_until > now:
    #         order = task.order_within_project
    #         task_ids_to_exclude.extend(Task.objects.filter(project=task.project, order_within_project__gte=order).values_list('id',flat=True))
    #
    # tasks = Task.objects.filter(status='A').exclude(id__in=task_ids_to_exclude)
    # # tasks = sorted(tasks, key=lambda t: t.score)
    # tasks_to_display = []
    # for task in tasks:


    today_data = {
        'tasks': tasks
    }
    return today_data