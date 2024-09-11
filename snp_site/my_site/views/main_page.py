from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
from models_app.models import Photo
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin




class MainPageView(CreateView,LoginRequiredMixin):
    model=Photo
    template_name="main_page.html"
    fields = ['photo', 'caption']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/'
    
    