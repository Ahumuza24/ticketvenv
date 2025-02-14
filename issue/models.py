from django.db import models
from users.models import User
import uuid

class Issue(models.Model):
    status_choices = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
    )

    category_choices = (
        ('Missing Marks', 'Missing Marks'),
        ('Appeals', 'Appeals'),
        ('Corrections.', 'Corrections.'),
    )

    
    issue_number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    issue_status = models.CharField(max_length=100, choices=status_choices, default='Pending')
    category = models.CharField(max_length=100, choices=category_choices, default='Academic')
    attached_file = models.FileField(upload_to='issue_attachments/', null=True, blank=True)

    def __str__(self):
        return self.title