from django.contrib import admin
from models_app.models import User, Photo, Comment, Like

admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Like)