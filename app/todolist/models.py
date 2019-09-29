from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class TodoList(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s' % (self.pk, self.title)


class Todo(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    title = models.CharField(max_length=200)
    todo_list = models.ForeignKey(
        TodoList, on_delete=models.PROTECT, related_name='todos')

    INCOMPLETE = 'IN'
    COMPLETED = 'CO'
    ARCHIVED = 'AR'
    TODO_STATUS_CHOICES = (
        (INCOMPLETE, 'Incompleto'),
        (COMPLETED, 'Terminado'),
        (ARCHIVED, 'Archivado'),
    )
    status = models.CharField(
        max_length=2, choices=TODO_STATUS_CHOICES, default=INCOMPLETE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s - %s (%s %s)' % (self.pk, self.todo_list.title, self.title, self.status)
