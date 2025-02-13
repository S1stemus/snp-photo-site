from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View
from models_app.models import Photo
from models_app.models.comment import Comment


class CommentView(View, LoginRequiredMixin):

    class_dict = {"photo": Photo, "comment": Comment}

    def post(self, request, pk):

        comment = request.POST.get("comment")
        content_type = request.POST.get("content_type")
        if content_type is None or content_type not in self.class_dict.keys():
            return HttpResponseBadRequest("Empty content_type")
        Comment.objects.create(
            user=request.user,
            comment=comment,
            content_type=ContentType.objects.get_for_model(
                self.class_dict[content_type]
            ),
            object_id=pk,
        )
        return redirect(request.META.get("HTTP_REFERER", "default_photo_page"))
