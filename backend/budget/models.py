from django.db import models
from django.utils import timezone

class Purchase(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'purchase'

class Budget(models.Model):
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    current_month_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_month_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.IntegerField(default=timezone.now().month)
    year = models.IntegerField(default=timezone.now().year)

    class Meta:
        unique_together = ('month', 'year')
        db_table = 'budget'
