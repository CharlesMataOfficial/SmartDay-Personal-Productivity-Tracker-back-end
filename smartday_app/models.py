from django.db import models
from django.contrib.auth.models import User

# ✅ Represents a "Task Menu" or "Routine Menu"
class Category(models.Model):
    CATEGORY_TYPE = [
        ('task', 'Task'),
        ('routine', 'Routine'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)  # e.g. "Task 1", "Routine 1"
    type = models.CharField(max_length=10, choices=CATEGORY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.name}"


# ✅ Represents the actual items inside each Task/Routine group
class Item(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    due_date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)  # optional for routines
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"
