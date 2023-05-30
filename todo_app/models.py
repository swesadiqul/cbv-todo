from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    WORK_STATUS = [
        ('', '-select work status-'),
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=WORK_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    yasin = models.Manager()

    def __str__(self):
        return self.title
