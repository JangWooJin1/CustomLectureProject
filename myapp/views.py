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

        if cursor.description is None:
            return None

        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

class MainPage(View):
    template_name = 'mainPage.html'

    def get(self, request):
        curriculum_list = Lecture.objects.values_list('lecture_curriculum', flat=True).distinct()

        campus_list = Lecture.objects.values_list('lecture_campus', flat=True).distinct()

        search_label_list = ["교과목", "학수번호", "교원명"]
        search_value_list = ["lecture_name", "lecture_code", "lecture_professor"]
        search_zip_list = zip(search_value_list, search_label_list)

        context = {
            'curriculum_list': curriculum_list,
            'campus_list': campus_list,
            'search_zip_list': search_zip_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


def get_classification_options(request):
    selected_value = request.GET.get('selected_value')

    read_query = """
    SELECT DISTINCT lecture_classification
    FROM myapp_lecture
    WHERE lecture_curriculum=%s
    """

    read_params = [selected_value]

    classification_list = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(classification_list, safe=False)


def get_univ_options(request):
    read_query = """
    SELECT DISTINCT lecture_univ
    FROM myapp_lecture
    WHERE lecture_curriculum="전공"
    """

    univ_list = execute_raw_sql_query(read_query)

    return JsonResponse(univ_list, safe=False)


def get_major_options(request):
    selected_value = request.GET.get('selected_value')

    read_query ="""
    SELECT DISTINCT lecture_major
    FROM myapp_lecture
    WHERE lecture_univ = %s
    """

    read_params = [selected_value]

    major_list = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(major_list, safe=False)

@csrf_exempt
def get_lecture(request):
    curriculum = request.POST.get('curriculum')
    classification = request.POST.get('classification')
    campus = request.POST.get('campus')
    univ = request.POST.get('univ')
    major = request.POST.get('major')
    searchCondition = request.POST.get('searchCondition')
    search = request.POST.get('search')

    read_query = "SELECT * FROM myapp_lecture WHERE 1=1"

    read_params = []

    if searchCondition and search:
        read_query += f" AND {searchCondition} LIKE %s"
        read_params.append(f'%{search}%')
    else:
        if curriculum != 'all':
            read_query += " AND lecture_curriculum = %s"
            read_params.append(curriculum)

        if classification != 'all':
            read_query += " AND lecture_classification = %s"
            read_params.append(classification)

        if campus != 'all':
            read_query += " AND lecture_campus = %s"
            read_params.append(campus)

        if (univ is not None) and univ != 'all' :
            read_query += " AND lecture_univ = %s"
            read_params.append(univ)

        if (major is not None) and major != 'all':
            read_query += " AND lecture_major = %s"
            read_params.append(major)

    lectures_json = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(lectures_json, safe=False)

@csrf_exempt
def add_userbasket(request):
    user_id = 'jang'
    lecture_code = request.POST.get('lecture_code')

    insert_query = """
    INSERT INTO myapp_userbasket (user_id_id, lecture_id_id)
    SELECT %s, l.lecture_id
    FROM myapp_lecture AS l
    WHERE l.lecture_code = %s
    """

    insert_params = [user_id, lecture_code]

    execute_raw_sql_query(insert_query,insert_params)

    read_query = """
       SELECT * 
       FROM myapp_userbasket
       INNER JOIN myapp_lecture ON myapp_userbasket.lecture_id_id = myapp_lecture.lecture_id
       WHERE myapp_userbasket.user_id_id = %s
       """

    read_params = [user_id]

    lectures_json = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(lectures_json, safe=False)
@csrf_exempt
def delete_userbasket(request):
    user_id = 'jang'
    lecture_code = request.POST.get('lecture_code')

    delete_query = """
    DELETE FROM myapp_userbasket
    WHERE user_id_id = %s AND lecture_id_id IN (
        SELECT l.lecture_id
        FROM myapp_lecture AS l
        WHERE l.lecture_code = %s
    )
    """

    delete_params = [user_id, lecture_code]

    execute_raw_sql_query(delete_query, delete_params)

    read_query = """
       SELECT * 
       FROM myapp_userbasket
       INNER JOIN myapp_lecture ON myapp_userbasket.lecture_id_id = myapp_lecture.lecture_id
       WHERE myapp_userbasket.user_id_id = %s
       """

    read_params = [user_id]

    lectures_json = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(lectures_json, safe=False)

