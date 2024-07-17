from django.http import HttpResponse
from django.views import View


class MainPageView(View):
    def get(self, request):
        breakpoint()
        return HttpResponse("result")