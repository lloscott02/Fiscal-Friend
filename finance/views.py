from django.shortcuts import render
from django.db.models import Sum
from .models import Category, Budget, Expense
from django.utils import timezone
import calendar

def landing_page(request):
    """View for the landing page."""
    return render(request, 'landing.html')

def dashboard(request):
    # Get current month and year
    today = timezone.now()
    current_month = today.strftime('%B')
    current_year = today.year
    
    # Get all categories
    categories = Category.objects.all()
    
    # Get current month's budget
    current_budget = Budget.objects.filter(month=current_month).first()
    
    # Get expenses for current month
    current_month_expenses = Expense.objects.filter(
        date__year=current_year,
        date__month=today.month
    )
    
    # Calculate total expenses
    total_expenses = current_month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate expenses by category
    expenses_by_category = {}
    for category in categories:
        category_expenses = current_month_expenses.filter(category=category)
        category_total = category_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_by_category[category.name] = category_total
    
    context = {
        'current_month': current_month,
        'current_year': current_year,
        'current_budget': current_budget,
        'total_expenses': total_expenses,
        'expenses_by_category': expenses_by_category,
        'categories': categories,
    }
    
    return render(request, 'finance/dashboard.html', context)
