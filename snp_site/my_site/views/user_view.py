from django.db.models import Count
from django.views.generic import DetailView
from models_app.models import User
from models_app.models.photo.fsm import State


class UserView(DetailView):
    model = User
    template_name = "user_page.html"
    slug_url_kwarg = "username"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.request.GET.get("filter")
        photos = self.get_object().photos.filter(
            state=State.APPROVED, user=self.request.user.id
        )
        if filter == "old":
            photos = photos.order_by("created_at")
        elif filter == "new":
            photos = photos.order_by("-created_at")
        elif filter == "popular":
            photos = photos.annotate(like_count=Count("like")).order_by("-like_count")
        context["photos"] = photos
        return context
