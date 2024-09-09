from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Purchase(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

class Budget(models.Model):
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_month_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_month_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
