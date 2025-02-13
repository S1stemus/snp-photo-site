from django.db.models import Count
from django.views.generic import ListView
from models_app.models import Photo
from models_app.models.photo.fsm import State


class PhotoListView(ListView):
    model = Photo
    template_name = "photo_list_page.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.request.GET.get("filter")
        photos = Photo.objects.filter(state=State.APPROVED)
        if filter == "old":
            photos = photos.order_by("created_at")
        elif filter == "new":
            photos = photos.order_by("-created_at")
        elif filter == "popular":
            photos = photos.annotate(like_count=Count("like")).order_by("-like_count")
        context["photos"] = photos
        return context
