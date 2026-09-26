# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    university = models.CharField(max_length=100, default='UNIBEN')
    level = models.CharField(max_length=10, blank=True)   # e.g., 100, 200
    department = models.CharField(max_length=100, blank=True)
    budget_min = models.IntegerField(null=True, blank=True)
    budget_max = models.IntegerField(null=True, blank=True)
    preferred_loc = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username