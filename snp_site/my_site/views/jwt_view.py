from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class JwtView(View):
    template_name = "registration/jwt.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return JsonResponse({"message": "success"})
