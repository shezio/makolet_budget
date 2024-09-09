from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Purchase, Budget
import json
from datetime import datetime

@csrf_exempt
def add_purchase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        date = data.get('date', datetime.now())
        budget = Budget.objects.first()
        current_month = datetime.now().month

        # Ensure the purchase does not exceed the remaining budget
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
        budget = Budget.objects.first()
        budget.limit = new_limit
        budget.save()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_budget(request):
    month = request.GET.get('month', datetime.now().month)
    year = request.GET.get('year', datetime.now().year)
    budget = Budget.objects.first()
    purchases = Purchase.objects.filter(date__month=month, date__year=year)
    current_month_spent = sum(purchase.amount for purchase in purchases)
    return JsonResponse({
        'limit': budget.limit,
        'current_month_spent': current_month_spent,
        'last_month_spent': budget.last_month_spent,
        'purchases': list(purchases.values())
    })
