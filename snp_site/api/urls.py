from snp_site.api.views.photo import RetreivePhotoView
from django.urls import path


urlpatterns=[
    path('photo/<int:id>/', RetreivePhotoView.as_view()),
]
