from django.urls import path
from .views import HomeView, CategoryRegisterView, LedgerRegisterView, LedgerUpdateView, LedgerDeleteView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('category/register/', CategoryRegisterView.as_view(), name='category_register'),
    path('ledger/register/', LedgerRegisterView.as_view(), name='ledger_register'),
    path('ledger/update/', LedgerUpdateView.as_view(), name='ledger_update'),
    path('ledger/delete/', LedgerDeleteView.as_view(), name='ledger_delete'),
]