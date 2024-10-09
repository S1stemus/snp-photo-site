from api.views.photo import RetreivePhotoView
from api.views.comment import RetreiveCommentView
from django.urls import path

from api.views.comment import RetreiveCommentView


urlpatterns=[
    path('photo/<int:id>/', RetreivePhotoView.as_view()),
    path('comments/<int:id>/', RetreiveCommentView.as_view())
]
