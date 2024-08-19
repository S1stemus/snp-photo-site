from django.contrib import admin
from models_app.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('comment', 'user', 'content_type', 'object_id')