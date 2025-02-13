from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from models_app.models import Photo


class MainPageView(CreateView, LoginRequiredMixin):
    model = Photo
    template_name = "main_page.html"
    fields = ["photo", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = "/photos/"
