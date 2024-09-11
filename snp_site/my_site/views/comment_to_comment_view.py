from django.shortcuts import redirect
from django.views import View
from models_app.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
class CommentToCommentView(View,LoginRequiredMixin):

    def post(self, request, pk):
        comment_text = request.POST.get('comment')      
        Comment.objects.create(
            user=request.user, 
            comment=comment_text,
            content_type=ContentType.objects.get_for_model(Comment), 
            object_id=pk
            )
        return redirect(request.META.get('HTTP_REFERER', 'default_photo_page'))  