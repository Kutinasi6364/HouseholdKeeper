import json
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from .models import Ledger, Category
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, ListView):
    """
    ホーム画面に表示する要素を調整

    Methods:
        get_context_data: 表示する要素を追加
    """
    model = Ledger
    template_name = 'home.html'
    context_object_name = 'ledgers'
    login_url = '/user/login/'

    def get_category_data(self, user, transaction_type, year, month):
        """カテゴリ別の収支データを集計し、円グラフ用データを生成"""
        category_data = Ledger.objects.filter(
            transaction_type=transaction_type, user=user, date__year=year, date__month=month
        ).values('category').annotate(total_amount=Sum('amount'))

        total = sum(item['total_amount'] for item in category_data) or 1
        return json.dumps({
            "labels": [item['category'] for item in category_data],
            "values": [round((item['total_amount'] / total) * 100, 2) for item in category_data]
        }, ensure_ascii=False)

    def get_context_data(self, **kwargs):
        """テンプレートに渡すデータを生成"""
        context = super().get_context_data(**kwargs)
        date = datetime.now()
        
        context.update({
            'year': date.year,
            'month': date.month,
            'income': Ledger.objects.filter(transaction_type='income', user=self.request.user, date__year=date.year, date__month=date.month).aggregate(Sum('amount')).get('amount__sum', 0) or 0,
            'expense': Ledger.objects.filter(transaction_type='expense', user=self.request.user, date__year=date.year, date__month=date.month).aggregate(Sum('amount')).get('amount__sum', 0) or 0,
            'income_category_data': self.get_category_data(self.request.user, 'income', date.year, date.month),
            'expense_category_data': self.get_category_data(self.request.user, 'expense', date.year, date.month),
            'categories': Category.objects.filter(user=self.request.user),
            'transactions': Ledger.objects.filter(user=self.request.user, date__year=date.year, date__month=date.month).order_by('-id'),
        })

        return context


class CategoryRegisterView(View):
    """
    カテゴリを調整

    Methods:
        post: カテゴリを登録
    """
    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('category')

        if not category_name:
            messages.error(request, 'カテゴリ名を入力してください。')
            return HttpResponseRedirect(reverse('home'))

        category, created = Category.objects.get_or_create(name=category_name, user=request.user)

        if created:
            category.save()
            messages.success(request, f'カテゴリ "{category_name}" が登録されました。')
        else:
            # 既存カテゴリの場合のメッセージ
            messages.info(request, f'カテゴリ "{category_name}" はすでに存在します。')

        # 登録後、home画面にリダイレクト
        return HttpResponseRedirect(reverse('home'))


class LedgerRegisterView(View):
    """
    取引情報を処理

    Methods:
        post: 取引情報を登録
    """
    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('category')
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        transaction_type = request.POST.get('transaction_type')

        if not category_name or not name or not amount or not date or not transaction_type:
            messages.error(request, f'必要な情報を入力してください。cateogory_id: {category_name} name: {name} amount: {amount} date: {date} transaction_type: {transaction_type}')
            return HttpResponseRedirect(reverse('home'))

        category = Category.objects.get(name=category_name)
        Ledger.objects.create(category=category, name=name, amount=amount, date=date, transaction_type=transaction_type, user=request.user)

        messages.success(request, f'取引 "{name}" が登録されました。')
        return HttpResponseRedirect(reverse('home'))

class LedgerUpdateView(View):
    """
    取引情報を更新

    Methods:
        post: 取引情報を更新
    """
    def post(self, request, *args, **kwargs):
        ledger_id = request.POST.get('id')
        ledger = Ledger.objects.get(id=ledger_id)

        category_name = request.POST.get('category')
        ledger.category = Category.objects.get(name=category_name)

        ledger.name = request.POST.get('name')
        ledger.amount = request.POST.get('amount')
        ledger.date = request.POST.get('date')
        ledger.transaction_type = request.POST.get('transaction_type')
        ledger.save()

        messages.success(request, f'取引 "{ledger.name}" が更新されました。')
        return HttpResponseRedirect(reverse('home'))

class LedgerDeleteView(View):
    """
    取引情報を削除

    Methods:
        post: 取引情報を削除
    """
    def post(self, request, *args, **kwargs):
        ledger_id = request.POST.get('id')
        ledger = Ledger.objects.get(id=ledger_id)
        ledger.delete()

        messages.success(request, f'取引 "{ledger.name}" が削除されました。')
        return HttpResponseRedirect(reverse('home'))