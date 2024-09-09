import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Purchase, Budget
from datetime import datetime
from pathlib import Path

# Load configuration
config_path = Path(__file__).resolve().parent / 'config.json'
with open(config_path) as config_file:
    config = json.load(config_file)

@csrf_exempt
def add_purchase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        date = data.get('date', datetime.now())
        budget = Budget.objects.first()
        current_month = datetime.now().month

        if budget.current_month_spent + amount > budget.limit:
            return JsonResponse({'error': 'Purchase exceeds the remaining budget'}, status=400)

        Purchase.objects.create(amount=amount, date=date)
        budget.current_month_spent += amount
        budget.save()
        return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def update_budget_limit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_limit = data.get('limit')
        budget, created = Budget.objects.get_or_create(id=1)
        budget.limit = new_limit
        budget.save()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_budget(request):
    month = request.GET.get('month', datetime.now().month)
    year = request.GET.get('year', datetime.now().year)
    budget, created = Budget.objects.get_or_create(
        id=1, 
        defaults={
            'limit': config['default_budget_limit'],
            'current_month_spent': config['initial_purchase_amount'],
            'last_month_spent': config['initial_purchase_amount']
        }
    )
    purchases = Purchase.objects.filter(date__month=month, date__year=year)
    current_month_spent = sum(purchase.amount for purchase in purchases)
    return JsonResponse({
        'limit': budget.limit,
        'current_month_spent': current_month_spent,
        'last_month_spent': budget.last_month_spent,
        'purchases': list(purchases.values())
    })
