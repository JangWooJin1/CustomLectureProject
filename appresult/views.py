from django.shortcuts import render
from .models import *
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from itertools import combinations, product
import math
import json

appName = "appresult"

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


# nCr의 모든 경우의수를 출력하는 함수
def find_combinations(lst, r):
    return list(combinations(lst, r))

#리스트 사이의 모든 경우의 수를 구해주는 함수
def generate_group_combinations(groups):
    result = list(product(*groups))
    return result

# myLecture와 allTimeTable를 형성하는 함수
def getGroupCombinations(basket_dict, group_credit_info_dict, credit_dict, required_group_list):
    basket_group_list = basket_dict.keys()

    # nCr에서 n값 구하기
    n = len(basket_group_list)

    # nCr에서 r값 범위 정하기 2~최대10
    min_r = 2
    max_r = -1
    if n > 10:
        max_r = 10
    else:
        max_r = n

    # 그룹끼리 조합 보기
    combination_group_list = []
    for r in range(min_r, max_r + 1):
        combination_group_list += find_combinations(basket_group_list, r)

    group_combinations = []
    # 생성된 그룹 조합에서 모든 강의 조합 보기
    min_credit = 3
    max_credit = 24

    if credit_dict:
        min_credit = int(credit_dict['전체']['min'])
        max_credit = int(credit_dict['전체']['max'])

    for combination in combination_group_list:
        if all(item in combination for item in required_group_list):
            groups = []
            groups_credit = 0
            for group in combination:
                groups.append(basket_dict[group])
                groups_credit += group_credit_info_dict[group]

            if (groups_credit >= min_credit and groups_credit <= max_credit):
                group_combinations.append(groups)

    return group_combinations

def getAllCombinations(group_combinations):
    all_combinations = []
    for groups in group_combinations:
        all_combinations += generate_group_combinations(groups)

    return all_combinations

def checkTimeConflict(selected_lectures, lecture):
    for selected_lecture in selected_lectures:
        if lecture['lecture_day'] == selected_lecture['lecture_day']:
            if lecture['lecture_start_time'] <= selected_lecture['lecture_end_time']  \
                    and lecture['lecture_end_time'] >= selected_lecture['lecture_start_time']:
                return True

    return False

def getValidCombinations(all_combinations, lecture_list):
    valid_combinations = []  # 유효한 Combination을 저장할 빈 리스트

    for Combination in all_combinations:
        selected_lectures = []
        is_valid = True

        for lecture in lecture_list:
            if lecture['lecture_id'] in Combination:
                isConflict = checkTimeConflict(selected_lectures, lecture)
                if isConflict == True:
                    is_valid = False
                    break
                else:
                    selected_lectures.append(lecture)
        if is_valid:
            valid_combinations.append(selected_lectures)

    return valid_combinations

class Result(View):
    template_name = 'resultPage.html'

    def get(self, request):
        user_id = request.session.get('_auth_user_id')

        group_list_query = f"""
        SELECT DISTINCT
            lg.lecture_code,
            lg.lecture_name
        FROM 
            appsearch_userbasket AS ub
        INNER JOIN
            appsearch_lectureItem AS li ON li.lecture_id = ub.lecture_id_id
        INNER JOIN
            appsearch_lectureGroup AS lg ON lg.lecture_code = li.lecture_code_id
        WHERE
            ub.user_id_id = %s
        """

        group_list_query_params = [user_id]

        group_list = execute_raw_sql_query(group_list_query, group_list_query_params)


        context = {
            'group_list' : group_list
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass

def calculate_group_combinations(basket_dict):
    basket_group_list = basket_dict.keys()

    # nCr에서 n값 구하기
    n = len(basket_group_list)

    # nCr에서 r값 범위 정하기 2~최대10
    min_r = 2
    max_r = -1
    if n > 10:
        max_r = 10
    else:
        max_r = n

    # 그룹끼리 조합 보기
    count_group_combination = 0
    for r in range(min_r, max_r + 1):
        count_group_combination += math.comb(n, r)

    return count_group_combination

def calculate_all_combinations(lecture_Combination_results):
    count_all_combination = 0
    for combination in lecture_Combination_results:
        temp = 1
        for group in combination:
            temp = temp * len(group)
        count_all_combination += temp

    return count_all_combination

@csrf_exempt
def get_lecture_combinations(request):
    user_id = request.session.get('_auth_user_id')
    campus = request.POST.get('campus')
    time = json.loads(request.POST.get('time'))
    credit = json.loads(request.POST.get('credit'))
    group = json.loads(request.POST.get('group'))

    lecture_list_query = f"""
    SELECT
        li.lecture_id,
        li.lecture_code_id,
        lg.lecture_name,
        lg.lecture_credit,
        li.lecture_professor,
        ls.lecture_room,
        ls.lecture_day,
        ls.lecture_start_time,
        ls.lecture_end_time
    FROM 
        appsearch_userbasket AS ub
    INNER JOIN
        appsearch_lectureItem AS li ON li.lecture_id = ub.lecture_id_id
    INNER JOIN
        appsearch_lectureGroup AS lg ON lg.lecture_code = li.lecture_code_id
    INNER JOIN
        appsearch_lectureItemSchedule AS ls ON li.lecture_id = ls.lecture_id_id
    WHERE
        ub.user_id_id = %s
    """

    lecture_list_query_params = [user_id]


    if campus != "전체":
        lecture_list_query += " AND li.lecture_campus = %s"
        lecture_list_query_params.append(campus)

    if time:
        lecture_list_query += """ AND li.lecture_id NOT IN (
            SELECT DISTINCT
                sls.lecture_id_id
            FROM 
                appsearch_lectureItemSchedule AS sls
            WHERE 
                (
        """

        conditions = []
        for day, time_range in time.items():
            start_time = float(time_range['start'])
            if (start_time <= 18):
                start_time -= 8
            else:
                start_time -= 7.5

            end_time = float(time_range['end'])
            if (end_time <= 18):
                end_time -= 8.5
            else:
                end_time -= 8

            condition = "(sls.lecture_day = %s AND (sls.lecture_start_time <= %s AND sls.lecture_end_time >= %s))\n"
            conditions.append(condition)
            lecture_list_query_params.append(day)
            lecture_list_query_params.append(end_time)
            lecture_list_query_params.append(start_time)


        lecture_list_query += " OR ".join(conditions)
        lecture_list_query += "))"


    lecture_list = execute_raw_sql_query(lecture_list_query, lecture_list_query_params)

    basket_dict = {}

    group_credit_info_dict = {}

    for item in lecture_list:
        lecture_id = item['lecture_id']
        lecture_code_id = item['lecture_code_id']

        if lecture_code_id not in basket_dict:
            basket_dict[lecture_code_id] = []

        if lecture_code_id not in group_credit_info_dict:
            group_credit_info_dict[lecture_code_id] = item['lecture_credit']

        if lecture_id not in basket_dict[lecture_code_id]:
            basket_dict[lecture_code_id].append(lecture_id)

    count_group_combinations = calculate_group_combinations(basket_dict)
    print(count_group_combinations)
    #@@@@@@@@그룹 조합 결과가 많으면 뒤의 알고리즘 종료 구현
    group_combinations= getGroupCombinations(basket_dict, group_credit_info_dict, credit, group)

    count_all_combinations = calculate_all_combinations(group_combinations)
    print(count_all_combinations)
    # @@@@@@@@최종 조합 결과가 많으면 뒤의 알고리즘 종료 구현
    all_combinations = getAllCombinations(group_combinations)

    valid_combinations = getValidCombinations(all_combinations, lecture_list)

    datas = {
        'count_all_combinations' : count_all_combinations,
        'valid_combinations' : valid_combinations
    }

    return JsonResponse(datas, safe=False)

@csrf_exempt
def add_user_timetable(request):
    lectures = list(json.loads(request.POST.get('lectures')))

    user_id = request.session.get('_auth_user_id')

    read_query = """
    SELECT MAX(class_num) AS max_num
    FROM appresult_mytimetable
    WHERE user_id_id = %s
    """

    read_params = [user_id]

    max_num_dict = execute_raw_sql_query(read_query, read_params)
    print(max_num_dict)
    if max_num_dict[0]['max_num']:
        max_num = max_num_dict[0]['max_num'] + 1
    else:
        max_num = 1

    insert_query = """
    INSERT INTO appresult_mytimetable(class_num, lecture_id_id, user_id_id)
    SELECT %s, lecture_id, %s
    FROM appsearch_lectureItem as li
    WHERE li.lecture_id IN %s
    """
    insert_params = [max_num, user_id, lectures]

    execute_raw_sql_query(insert_query, insert_params)

    data = {
        'success' : '강의 추가 성공'
    }

    return JsonResponse(data, safe=False)