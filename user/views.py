from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

class SignUpView(CreateView):
    """
    ユーザー登録処理

    Methods:
        form_valid: ユーザー登録処理
    """
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')