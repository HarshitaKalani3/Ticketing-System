from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, default="OPEN") # e.g. OPEN, RESOLVED
    priority = models.CharField(max_length=50, default="MEDIUM")
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ManyToManyField(User, related_name='assigned_tickets', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tickets'

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)