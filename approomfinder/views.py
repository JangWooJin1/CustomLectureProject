from django.shortcuts import render
from django.views import View

# Create your views here.

class RoomFinder(View):
    template_name = "roomfinderPage.html"

    def get(self, request):
        return render(request, self.template_name)

    def POST(self, request):
        pass
