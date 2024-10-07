from rest_framework.views import APIView
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from snp_site.api.serializers.photo_serializer import PhotoSerializer
from snp_site.api.services.photo.show import ShowPhotoService
from snp_site.models_app.models.photo.models import Photo

class RetreivePhotoView(APIView):

    def get(self, request, *args, **kwargs):
        outcome=ServiceOutcome(ShowPhotoService,{'id':kwargs['id']} )
        return Response(PhotoSerializer(outcome.result).data)
    
    # def delete()


