from django.urls import path
from .views import (
    ExpenseListCreate, ExpenseDelete, RegisterView,
    login_view, register_view, dashboard, logout_view,
    ExpenseCreateView
)

urlpatterns = [
    # API endpoints
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/expenses/', ExpenseListCreate.as_view(), name='expense-list-create'),
    path('api/expenses/<int:pk>/', ExpenseDelete.as_view(), name='expense-delete'),
    
    # Frontend views
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    
    # New expense routes
    path('expenses/add/', ExpenseCreateView.as_view(), name='add_expense'),
    path('expenses/<int:pk>/delete/', ExpenseDelete.as_view(), name='delete_expense'),
]