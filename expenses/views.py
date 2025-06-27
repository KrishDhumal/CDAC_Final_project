# expenses/views.py

# 🔹 For REST API views
from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer
from django.contrib.auth.models import User

# 🔹 For frontend-based views
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, ExpenseForm
from django.db.models import Sum
from datetime import datetime

# ----------------------------
# ✅ REST API Views
# ----------------------------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseListCreate(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseDelete(generics.DestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

# ----------------------------
# ✅ Template-Based Views (Frontend)
# ----------------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    categories = Expense.objects.filter(user=request.user).values_list('category', flat=True).distinct()
    
    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'categories': categories
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'expense': expense})

def logout_view(request):
    logout(request)
    return redirect('login')

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'add_expense.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)