from django.db import models
from django.contrib.auth.models import User


# 取引記録
class Ledger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='登録ユーザー') # 登録ユーザー Userと削除連携
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='カテゴリ') # カテゴリ
    name = models.CharField(max_length=100,verbose_name='取引名') # 取引名
    amount = models.IntegerField(default=0,verbose_name='取引金額') # 取引金額
    date = models.DateField(verbose_name='取引日') # 取引日
    transaction_type = models.CharField(choices=[('income', '支出'), ('expense', '収入')], max_length=10,verbose_name='取引種別')

    def __str__(self):
        return self.name


# 取引カテゴリ
class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name