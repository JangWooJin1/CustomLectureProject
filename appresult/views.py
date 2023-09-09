from django.shortcuts import render
from .models import *
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from itertools import combinations, product
import copy

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
def getAllLectureCombinations(basket_dict):
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

    result = []
    # 생성된 그룹 조합에서 모든 강의 조합 보기
    for combination in combination_group_list:
        groups = []
        for group in combination:
            groups.append(basket_dict[group])
        result += generate_group_combinations(groups)

    return result

def checkTimeConflict(selected_lectures, lecture):
    for selected_lecture in selected_lectures:
        if lecture['lecture_day'] == selected_lecture['lecture_day']:
            if lecture['lecture_start_time'] <= selected_lecture['lecture_end_time']  \
                    and lecture['lecture_end_time'] >= selected_lecture['lecture_start_time']:
                return True

    return False

def getValidLectureCombinations(lecture_Combination_results, lecture_list):
    valid_combinations = []  # 유효한 Combination을 저장할 빈 리스트

    for Combination in lecture_Combination_results:
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
        user_id = 'jang'

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


def get_lecture_combinations(request):
    user_id = 'jang'

    lecture_list_query = f"""
    SELECT
        li.lecture_id,
        li.lecture_code_id,
        lg.lecture_name,
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

    lecture_list = execute_raw_sql_query(lecture_list_query, lecture_list_query_params)

    basket_dict = {}

    for item in lecture_list:
        lecture_id = item['lecture_id']
        lecture_code_id = item['lecture_code_id']

        if lecture_code_id not in basket_dict:
            basket_dict[lecture_code_id] = []

        if lecture_id not in basket_dict[lecture_code_id]:
            basket_dict[lecture_code_id].append(lecture_id)

    lecture_Combination_results = getAllLectureCombinations(basket_dict)

    valid_lecture_Combination_results = getValidLectureCombinations(lecture_Combination_results, lecture_list)

    return JsonResponse(valid_lecture_Combination_results, safe=False)