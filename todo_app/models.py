from django.db import models

class Todo(models.Model):
    WORK_STATUS = [
        ('', '-select work status-'),
        ('P', 'Pending'),
        ('C', 'Completed'),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=WORK_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    yasin = models.Manager()

    def __str__(self):
        return self.title
