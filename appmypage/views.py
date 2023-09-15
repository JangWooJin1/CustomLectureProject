from django.shortcuts import render
from django.views import View

# Create your views here.
class Mypage(View):
    template_name = 'myTimeTablePage.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
