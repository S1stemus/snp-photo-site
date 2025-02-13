from django.shortcuts import redirect
from django.views import View
from models_app.models import Like, Photo


class LikeView(View):
    def post(self, request, pk):
        photo = Photo.objects.get(pk=pk)
        like = Like.objects.filter(user=request.user, photo=photo)
        if like:
            like.delete()
        else:
            Like.objects.create(user=request.user, photo=photo)

        return redirect(request.META.get("HTTP_REFERER", "default_photo_page"))
