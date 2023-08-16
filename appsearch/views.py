from django.shortcuts import render
from .models import Lecture
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

appName = "appsearch"

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

class Search(View):
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

    read_query = f"""
    SELECT DISTINCT lecture_classification
    FROM {appName}_lecture
    WHERE lecture_curriculum=%s
    """

    read_params = [selected_value]

    classification_list = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(classification_list, safe=False)


def get_univ_options(request):
    read_query = f"""
    SELECT DISTINCT lecture_univ
    FROM {appName}_lecture
    WHERE lecture_curriculum="전공"
    """

    univ_list = execute_raw_sql_query(read_query)

    return JsonResponse(univ_list, safe=False)


def get_major_options(request):
    selected_value = request.GET.get('selected_value')

    read_query =f"""
    SELECT DISTINCT lecture_major
    FROM {appName}_lecture
    WHERE lecture_univ = %s
    """

    read_params = [selected_value]

    major_list = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(major_list, safe=False)

@csrf_exempt
def get_lecture(request):
    code = request.POST.get('lecture_code')

    read_query = f"""
    SELECT
        lecture_code,
        lecture_number,
        lecture_professor,
        lecture_campus,
        lecture_remark,
        GROUP_CONCAT(
            DISTINCT CONCAT(lecture_day, ' ', lecture_start_time, '-', lecture_end_time)
            ORDER BY lecture_day
            SEPARATOR ', '
        ) AS combined_lecture_times,
        GROUP_CONCAT(
            DISTINCT lecture_room
            ORDER BY lecture_room 
            SEPARATOR ', '
        ) AS combined_lecture_rooms
    FROM
        {appName}_lecture
    INNER JOIN 
        {appName}_lecturetime ON {appName}_lecture.lecture_id = {appName}_lecturetime.lecture_id_id
    INNER JOIN 
        {appName}_lectureroom ON {appName}_lecture.lecture_id = {appName}_lectureroom.lecture_id_id
    WHERE lecture_code = %s
    GROUP BY lecture_id
    """

    read_params = [code]

    lectures = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(lectures, safe=False)

@csrf_exempt
def get_lecture_group(request):
    curriculum = request.POST.get('curriculum')
    classification = request.POST.get('classification')
    campus = request.POST.get('campus')
    univ = request.POST.get('univ')
    major = request.POST.get('major')
    searchCondition = request.POST.get('searchCondition')
    search = request.POST.get('search')

    read_query = f"""
    SELECT DISTINCT
        lecture_curriculum,
        lecture_classification,
        lecture_code,
        lecture_name,
        lecture_credit
    FROM {appName}_lecture 
    WHERE 1=1
    """

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

    lecture_group = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(lecture_group, safe=False)

@csrf_exempt
def add_userbasket(request):
    user_id = 'jang'
    lecture_code = request.POST.get('lecture_code')
    lecture_number = request.POST.get('lecture_number')

    insert_query = f"""
    INSERT INTO {appName}_userbasket (user_id_id, lecture_id_id)
    SELECT %s, l.lecture_id
    FROM {appName}_lecture AS l
    WHERE l.lecture_code = %s
    """

    insert_params = [user_id, lecture_code]

    if lecture_number:
        insert_query += " AND l.lecture_number = %s"
        insert_params.append(lecture_number)

    execute_raw_sql_query(insert_query,insert_params)

    read_codes_query = f"""
    SELECT DISTINCT lecture_code
    FROM {appName}_userbasket
    INNER JOIN {appName}_lecture ON {appName}_userbasket.lecture_id_id = {appName}_lecture.lecture_id
    WHERE {appName}_userbasket.user_id_id = %s
    """

    read_params = [user_id]

    lecture_codes = execute_raw_sql_query(read_codes_query, read_params)

    lecture_groups = []
    read_group_query = f"""
     SELECT
         lecture_id,
         lecture_curriculum,
         lecture_classification,
         lecture_code,
         lecture_number,
         lecture_name,
         lecture_professor,
         lecture_campus,
         lecture_credit,
         lecture_univ,
         lecture_major,
         lecture_remark,
         GROUP_CONCAT(
             DISTINCT CONCAT(lecture_day, ' ', lecture_start_time, '-', lecture_end_time)
             ORDER BY lecture_day
             SEPARATOR ', '
         ) AS combined_lecture_times,
         GROUP_CONCAT(
             DISTINCT lecture_room
             ORDER BY lecture_room 
             SEPARATOR ', '
         ) AS combined_lecture_rooms
     FROM
         {appName}_lecture
     INNER JOIN 
         {appName}_userbasket ON {appName}_lecture.lecture_id = {appName}_userbasket.lecture_id_id
     INNER JOIN 
         {appName}_lecturetime ON {appName}_lecture.lecture_id = {appName}_lecturetime.lecture_id_id
     INNER JOIN 
         {appName}_lectureroom ON {appName}_lecture.lecture_id = {appName}_lectureroom.lecture_id_id
     WHERE 
         {appName}_userbasket.user_id_id = %s AND lecture_code = %s
     GROUP BY
         lecture_id
     """
    read_params.append('')

    for lecture_code in lecture_codes:
        read_params[-1] = lecture_code['lecture_code']
        lecture_groups.append(execute_raw_sql_query(read_group_query, read_params))

    return JsonResponse(lecture_groups, safe=False)

@csrf_exempt
def delete_userbasket(request):
    user_id = 'jang'
    lecture_code = request.POST.get('lecture_code')
    lecture_number = request.POST.get('lecture_number')

    delete_query = f"""
    DELETE {appName}_userbasket
    FROM {appName}_userbasket
    INNER JOIN {appName}_lecture ON {appName}_userbasket.lecture_id_id = {appName}_lecture.lecture_id
    WHERE user_id_id = %s AND lecture_code = %s
    """

    delete_params = [user_id, lecture_code]

    if lecture_number:
        delete_query += " AND lecture_number = %s"
        delete_params.append(lecture_number)

    execute_raw_sql_query(delete_query, delete_params)

    read_codes_query = f"""
    SELECT DISTINCT lecture_code
    FROM {appName}_userbasket
    INNER JOIN {appName}_lecture ON {appName}_userbasket.lecture_id_id = {appName}_lecture.lecture_id
    WHERE {appName}_userbasket.user_id_id = %s
    """

    read_params = [user_id]

    lecture_codes = execute_raw_sql_query(read_codes_query, read_params)

    lecture_groups = []

    read_group_query = f"""
     SELECT
         lecture_id,
         lecture_curriculum,
         lecture_classification,
         lecture_code,
         lecture_number,
         lecture_name,
         lecture_professor,
         lecture_campus,
         lecture_credit,
         lecture_univ,
         lecture_major,
         lecture_remark,
         GROUP_CONCAT(
             DISTINCT CONCAT(lecture_day, ' ', lecture_start_time, '-', lecture_end_time)
             ORDER BY lecture_day
             SEPARATOR ', '
         ) AS combined_lecture_times,
         GROUP_CONCAT(
             DISTINCT lecture_room
             ORDER BY lecture_room 
             SEPARATOR ', '
         ) AS combined_lecture_rooms
     FROM
         {appName}_lecture
     INNER JOIN 
         {appName}_userbasket ON {appName}_lecture.lecture_id = {appName}_userbasket.lecture_id_id
     INNER JOIN 
         {appName}_lecturetime ON {appName}_lecture.lecture_id = {appName}_lecturetime.lecture_id_id
     INNER JOIN 
         {appName}_lectureroom ON {appName}_lecture.lecture_id = {appName}_lectureroom.lecture_id_id
     WHERE 
         {appName}_userbasket.user_id_id = %s AND lecture_code = %s
     GROUP BY
         lecture_id
     """

    read_params.append('')

    for lecture_code in lecture_codes:
        read_params[-1] = lecture_code['lecture_code']
        lecture_groups.append(execute_raw_sql_query(read_group_query, read_params))

    return JsonResponse(lecture_groups, safe=False)

