from django.shortcuts import render
from .models import *
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
        curriculum_list_query = f"""
        SELECT DISTINCT lecture_curriculum
        FROM {appName}_lectureGroup
        """

        curriculum_list = execute_raw_sql_query(curriculum_list_query)

        campus_list_query = f"""
        SELECT DISTINCT lecture_campus
        FROM {appName}_lectureItem
        """

        campus_list = execute_raw_sql_query(campus_list_query)

        search_label_list = ["교과목", "학수번호"]
        search_value_list = ["lecture_name", "lecture_code", "lecture_professor"]
        search_zip_list = zip(search_value_list, search_label_list)

        user_id = request.session.get('user_id')
        userbasket_group_list = get_userbasket_group(user_id)

        context = {
            'curriculum_list': curriculum_list,
            'campus_list': campus_list,
            'search_zip_list': search_zip_list,
            'userbasket_group_list': userbasket_group_list,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


def get_classification_options(request):
    selected_value = request.GET.get('selected_value')

    read_query = f"""
    SELECT DISTINCT lecture_classification
    FROM {appName}_lectureGroup
    WHERE lecture_curriculum=%s
    """

    read_params = [selected_value]

    classification_list = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(classification_list, safe=False)


def get_univ_options(request):
    read_query = f"""
    SELECT DISTINCT lecture_univ
    FROM {appName}_lectureGroup
    WHERE lecture_curriculum="전공"
    """

    univ_list = execute_raw_sql_query(read_query)

    return JsonResponse(univ_list, safe=False)


def get_major_options(request):
    selected_value = request.GET.get('selected_value')

    read_query =f"""
    SELECT DISTINCT lecture_major
    FROM {appName}_lectureGroup
    WHERE lecture_univ = %s
    """

    read_params = [selected_value]

    major_list = execute_raw_sql_query(read_query, read_params)

    return JsonResponse(major_list, safe=False)

@csrf_exempt
def get_lecture_item(request):
    code = request.POST.get('lecture_code')
    campus = request.POST.get('campus')

    read_query = f"""
    SELECT
        lecture_id,
        lecture_code_id,
        lecture_number,
        lecture_professor,
        lecture_campus,
        lecture_remark,
        GROUP_CONCAT(
            CONCAT(lecture_day, ' ', lecture_start_time, '-', lecture_end_time)
            SEPARATOR ', '
        ) AS combined_lecture_times,
        GROUP_CONCAT(
            lecture_room
            SEPARATOR ', '
        ) AS combined_lecture_rooms
    FROM
        {appName}_lectureItem
    INNER JOIN 
        {appName}_lectureItemSchedule ON {appName}_lectureItem.lecture_id = {appName}_lectureItemSchedule.lecture_id_id
    WHERE lecture_code_id = %s
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
    SELECT
        lecture_curriculum,
        lecture_classification,
        lecture_code,
        lecture_name,
        lecture_credit
    FROM {appName}_lectureGroup
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

def get_userbasket_group(user_id, lecture_code=None):
    read_query = f"""
    SELECT DISTINCT
        lecture_curriculum,
        lecture_classification,
        lecture_code,
        lecture_name,
        lecture_credit
    FROM  
        {appName}_userbasket
    INNER JOIN 
        appaccount_user on {appName}_userbasket.user_id_id = appaccount_user.user_id 
    INNER JOIN 
        {appName}_lectureItem on {appName}_userbasket.lecture_id_id = {appName}_lectureItem.lecture_id
    INNER JOIN 
        {appName}_lectureGroup on {appName}_lectureItem.lecture_code_id = {appName}_lectureGroup.lecture_code
    WHERE
        user_id = %s
    """

    read_params = [user_id]

    if(lecture_code):
        read_query += " AND lecture_code = %s"
        read_params.append(lecture_code)

    basket_group = execute_raw_sql_query(read_query, read_params)

    return basket_group


def get_userbasket_item(user_id, lecture_code, lecture_number=None):
    read_query = f"""
    SELECT
        lecture_code_id,
        lecture_number,
        lecture_professor,
        lecture_campus,
        lecture_remark,
        GROUP_CONCAT(
            DISTINCT CONCAT(lecture_day, ' ', lecture_start_time, '-', lecture_end_time)
            SEPARATOR ', '
        ) AS combined_lecture_times,
        GROUP_CONCAT(
            DISTINCT lecture_room
            SEPARATOR ', '
        ) AS combined_lecture_rooms
    FROM  
        {appName}_userbasket
    INNER JOIN 
        appaccount_user on {appName}_userbasket.user_id_id = appaccount_user.user_id 
    INNER JOIN 
        {appName}_lectureItem on {appName}_userbasket.lecture_id_id = {appName}_lectureItem.lecture_id
    INNER JOIN 
        {appName}_lectureItemSchedule ON {appName}_lectureItem.lecture_id = {appName}_lectureItemSchedule.lecture_id_id
    WHERE 
        user_id = %s AND lecture_code_id = %s
    """

    read_params = [user_id, lecture_code]

    if lecture_number:
        read_query += " AND lecture_number = %s"
        read_params.append(lecture_number)

    read_query += " GROUP BY lecture_id"

    basket_item = execute_raw_sql_query(read_query, read_params)

    return basket_item

@csrf_exempt
def get_userbasket_items(request):
    user_id = request.session.get('user_id')
    lecture_code = request.POST.get('lecture_code')

    basket_items = get_userbasket_item(user_id, lecture_code)

    return JsonResponse(basket_items, safe=False)

@csrf_exempt
def add_userbasket(request):
    user_id = request.session.get('user_id')
    lecture_code = request.POST.get('lecture_code')
    lecture_number = request.POST.get('lecture_number')
    lecture_campus = request.POST.get('campus')

    insert_query = f"""
    INSERT INTO {appName}_userbasket (user_id_id, lecture_id_id)
    SELECT DISTINCT %s, l.lecture_id
    FROM {appName}_lectureItem AS l
    JOIN {appName}_lectureItemSchedule AS lt ON l.lecture_id = lt.lecture_id_id
    WHERE l.lecture_code_id = %s AND lt.lecture_day IS NOT NULL
    """

    insert_params = [user_id, lecture_code]

    if lecture_number:
        insert_query += " AND l.lecture_number = %s"
        insert_params.append(lecture_number)

    if lecture_campus:
        insert_query += " AND l.lecture_campus = %s"
        insert_params.append(lecture_campus)

    execute_raw_sql_query(insert_query, insert_params)

    response_data = {'message': 'Success'}
    return JsonResponse(response_data)

    # if lecture_number:
    #     basket_item = get_userbasket_item(user_id, lecture_code, lecture_number)
    #     return JsonResponse(basket_item, safe=False)
    # else:
    #     basket_group = get_userbasket_group(user_id, lecture_code)
    #     return JsonResponse(basket_group, safe=False)

@csrf_exempt
def delete_userbasket(request):
    user_id = request.session.get('user_id')
    lecture_code = request.POST.get('lecture_code')
    lecture_number = request.POST.get('lecture_number')

    delete_query = f"""
    DELETE {appName}_userbasket
    FROM {appName}_userbasket
    INNER JOIN {appName}_lectureItem ON {appName}_userbasket.lecture_id_id = {appName}_lectureItem.lecture_id
    WHERE user_id_id = %s AND lecture_code_id = %s
    """

    delete_params = [user_id, lecture_code]

    if lecture_number:
        delete_query += " AND lecture_number = %s"
        delete_params.append(lecture_number)

    execute_raw_sql_query(delete_query, delete_params)

    return JsonResponse([], safe=False)