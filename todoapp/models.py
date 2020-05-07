from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save

class UserInfo(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='userinfo')
    email_confirmed = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)

class Goal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_goals")
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    order_number = models.IntegerField(blank=True, null=True)
    COMPLETE = 'C'
    ACTIVE = 'A'
    DELETED = 'D'
    STATUS = [
        (COMPLETE, 'complete'),
        (ACTIVE, 'active'),
        (DELETED, 'deleted')
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )
    # dream, work, health, family, leisure, other
    # category =


class Project(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, related_name="goal_projects")
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    goal_kudos = models.IntegerField(blank=True, null=True)
    COMPLETE = 'C'
    ACTIVE = 'A'
    DELETED = 'D'
    STATUS = [
        (COMPLETE, 'complete'),
        (ACTIVE, 'active'),
        (DELETED, 'deleted')
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name="project_tasks")
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    not_until = models.DateTimeField(blank=True, null=True)
    order_within_project = models.IntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    COMPLETE = 'C'
    ACTIVE = 'A'
    DELETED = 'D'
    STATUS = [
        (COMPLETE, 'complete'),
        (ACTIVE, 'active'),
        (DELETED, 'deleted')
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=ACTIVE
    )

    @property
    def duration_string(self):
        if self.duration_minutes:
            hours = self.duration_minutes // 60
            minutes = self.duration_minutes % 60
            return ''.join([str(hours), "h ", str(minutes), "m"])
        else:
            return ''

    def rearrange_tasks_order(self):
        if not self.order_within_project:
            self.order_within_project = 1
            self.save()
        this_task_order = self.order_within_project
        all_tasks = Task.objects.filter(project=self.project, status__in=['A', 'C']).order_by(
            'order_within_project').exclude(id=self.id)
        other_tasks_count = all_tasks.count() + 1
        print(other_tasks_count)
        print(this_task_order)
        if this_task_order > other_tasks_count > 0:
            this_task_order = other_tasks_count
            self.order_within_project = other_tasks_count
            self.save()
        counter = 1
        for task in all_tasks:
            if task == self:
                continue
            if counter == this_task_order:
                counter = counter + 1
            task.order_within_project = counter
            task.save()
            counter = counter + 1

@receiver(post_save, sender=User)
def save_user_info(sender, instance, **kwargs):
    instance.userinfo.save()