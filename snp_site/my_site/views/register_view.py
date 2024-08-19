from multiprocessing import context
from django.views import View
from my_site.forms.UserCreationForm import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login


class RegisterView(View):
    template_name='registration/register.html'
    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main_page')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
