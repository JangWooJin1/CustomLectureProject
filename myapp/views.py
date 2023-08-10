from django.shortcuts import render
from .models import Lecture
from django.views import View
from django.http import JsonResponse

# Create your views here.
class mainPage(View):
    template_name = 'mainPage.html'

    def get(self, request):
        curriculum_list = Lecture.objects.values_list('lecture_curriculum', flat=True).distinct()
        campus_list = Lecture.objects.values_list('lecture_campus', flat=True).distinct()

        search_label_list = ["교과목", "학수번호", "교원명"]
        search_value_list = ["lecture_name", "lecture_code", "lecture_professor"]
        search_zip_list = zip(search_value_list, search_label_list)

        context = {
            'curriculum_list' : curriculum_list,
            'campus_list' : campus_list,
            'search_zip_list' : search_zip_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


def get_classification_options(request):
    selected_value = request.GET.get('selected_value')
    classification_list = Lecture.objects.filter(lecture_curriculum = selected_value).values_list('lecture_classification', flat=True).distinct()
    options = [{"value" : classification, "label" : classification} for classification in classification_list]

    return JsonResponse(options, safe=False)


def get_univ_options(request):
    univ_list = Lecture.objects.filter(lecture_curriculum = "전공").values_list('lecture_univ', flat=True).distinct()
    options = [{"value" : univ, "label":univ} for univ in univ_list]

    return JsonResponse(options, safe=False)


def get_major_options(request):
    selected_value = request.GET.get('selected_value')
    major_list = Lecture.objects.filter(lecture_univ = selected_value).values_list('lecture_major', flat=True).distinct()
    options = [{"value" : major, "label" : major} for major in major_list]

    return JsonResponse(options, safe=False)
