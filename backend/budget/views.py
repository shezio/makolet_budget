import logging
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
        data = json.loads(request.body)
        try:
            amount = int(data.get('amount'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid amount. It must be a number.'}, status=400)
        
        date = data.get('date')
        month = int(date.split('-')[1])
        year = int(date.split('-')[0])

        try:
            budget = Budget.objects.get(month=month, year=year)
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget for the specified month and year does not exist.'}, status=400)

        if amount < 0 and abs(amount) > budget.current_month_spent:
            return JsonResponse({'error': 'Cannot reduce spent amount below zero.'}, status=400)
        if budget.current_month_spent + amount > budget.limit:
            return JsonResponse({'error': 'Purchase amount exceeds budget limit.'}, status=400)

        # Add the purchase logic here
        budget.current_month_spent += amount
        budget.save()

        return JsonResponse({'success': 'Purchase added successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def update_budget_limit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_limit = data.get('limit')
        month = data.get('month')
        year = data.get('year')

        try:
            budget = Budget.objects.get(month=month, year=year)
            budget.limit = new_limit
            budget.save()
            return JsonResponse({'success': 'Budget limit updated successfully.'})
        except Budget.DoesNotExist:
            return JsonResponse({'error': 'Budget for the specified month and year does not exist.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

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