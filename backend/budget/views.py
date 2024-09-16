import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Purchase, Budget
import json
from datetime import datetime
from pathlib import Path
from decimal import Decimal

# Load configuration
config_path = Path(__file__).resolve().parent / 'config.json'
with open(config_path, encoding='utf8') as config_file:
    config = json.load(config_file)

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def add_purchase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount'))
            date = datetime.strptime(data.get('date'), '%Y-%m-%d') if 'date' in data else datetime.now()
            month = date.month
            year = date.year

            budget, created = Budget.objects.get_or_create(month=month, year=year, defaults={'limit': 1000}) # pylint: disable=no-member

            if budget.current_month_spent + amount > budget.limit:
                return JsonResponse({'error': 'Purchase exceeds the remaining budget'}, status=400)

            Purchase.objects.create(amount=amount, date=date) # pylint: disable=no-member
            budget.current_month_spent += amount
            budget.save()
            return JsonResponse({'status': 'success'}, status=201)
        except Exception as e:
            logger.error(f"Error adding purchase: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_budget_limit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_limit = data.get('limit')
        month = data.get('month', datetime.now().month)
        year = data.get('year', datetime.now().year)
        budget, created = Budget.objects.get_or_create(month=month, year=year) # pylint: disable=no-member
        budget.limit = new_limit
        budget.save()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_budget(request):
    month = int(request.GET.get('month', datetime.now().month))
    year = int(request.GET.get('year', datetime.now().year))
    budget, created = Budget.objects.get_or_create( # pylint: disable=no-member
        month=month, year=year,
        defaults={
            'limit': 1000,
            'current_month_spent': 0,
            'last_month_spent': 0
        }
    )
    purchases = Purchase.objects.filter(date__month=month, date__year=year) # pylint: disable=no-member
    current_month_spent = sum(purchase.amount for purchase in purchases)
    return JsonResponse({
        'limit': budget.limit,
        'current_month_spent': current_month_spent,
        'last_month_spent': budget.last_month_spent,
        'purchases': list(purchases.values())
    })