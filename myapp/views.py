from django.shortcuts import render
from .models import Lecture
from django.views import View
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db import connection

def execute_raw_sql_query(query, params=None):
    with connection.cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

# Create your views here.
class Login(View):
    pass

class MainPage(View):
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

@csrf_exempt
def get_lecture(request):
    curriculum = request.POST.get('curriculum')
    classification = request.POST.get('classification')
    campus = request.POST.get('campus')
    univ = request.POST.get('univ')
    major = request.POST.get('major')
    searchCondition = request.POST.get('searchCondition')
    search = request.POST.get('search')

    # 필터링 조건을 저장할 딕셔너리 생성
    filter_kwargs = {}

    # 검색값이 존재하면 해당 조건 추가
    if searchCondition and search:
        filter_kwargs[searchCondition + '__icontains'] = search

    else:
        # curriculum 값이 "all"이 아니면 curriculum 조건 추가
        if curriculum != 'all':
            filter_kwargs['lecture_curriculum'] = curriculum

        # classification 값이 "all"이 아니면 classification 조건 추가
        if classification != 'all':
            filter_kwargs['lecture_classification'] = classification

        # campus 값이 "all"이 아니면 campus 조건 추가
        if campus != 'all':
            filter_kwargs['lecture_campus'] = campus

        # univ 값이 "all"이 아니면 univ 조건 추가
        if univ != 'all':
            filter_kwargs['lecture_univ'] = univ

        # major 값이 "all"이 아니면 major 조건 추가
        if major != 'all':
            filter_kwargs['lecture_major'] = major


    # 조건에 맞는 레코드를 가져옵니다.
    lectures = Lecture.objects.filter(**filter_kwargs)

    # lecture_code_list = lectures.values_list('lecture_code',  flat=True).distinct()
    #
    # lecture_group_list = []
    # for lecture_code in lecture_code_list:
    #     lecture_group = Lecture.objects.filter(**filter_kwargs, lecture_code=lecture_code)
    #     lecture_group_json = serializers.serialize("json", lecture_group)
    #
    #     lecture_group_list.append(lecture_group_json)
    #     lecture_group_list.append(lecture_group)

    # Lecture 모델 인스턴스를 JSON 형식으로 변환
    lectures_json = serializers.serialize("json", lectures)
    return JsonResponse(lectures_json, safe=False)
    #return JsonResponse(lecture_group_list, safe=False)

@csrf_exempt
def add_userbasket(request):
    user_id = 'jang'
    lecture_code = request.POST.get('lecture_code')

    lectures_json = []
    return JsonResponse(lectures_json, safe=False)



