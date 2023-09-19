from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# Create your views here.
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

class Mypage(View):
    template_name = 'myTimeTablePage.html'

    def get(self, request):
        user_id = request.session.get('_auth_user_id')

        read_query = """
            SELECT
                mt.class_num,
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
                appresult_mytimetable AS mt
            INNER JOIN
                appsearch_lectureItem AS li ON li.lecture_id = mt.lecture_id_id
            INNER JOIN
                appsearch_lectureGroup AS lg ON lg.lecture_code = li.lecture_code_id
            INNER JOIN
                appsearch_lectureItemSchedule AS ls ON li.lecture_id = ls.lecture_id_id
            WHERE
                mt.user_id_id = %s
        """

        read_params = [user_id]

        lecture_list = execute_raw_sql_query(read_query, read_params)


        timetable_dict = {}

        for lecture in lecture_list:
            class_num = lecture['class_num']

            if class_num not in timetable_dict:
                timetable_dict[class_num] = []

            timetable_dict[class_num].append(lecture)


        context = {
            'timetable_dict': timetable_dict
        }


        return render(request, self.template_name, context)

    def post(self, request):
        pass


def delete_timetable(request):
    user_id = request.session.get('user_id')
    class_num = request.GET.get('class_num')

    delete_timetable_query = """
        DELETE FROM appresult_mytimetable
        WHERE user_id_id = %s AND class_num = %s
    """

    delete_timetable_params = [user_id, class_num]

    execute_raw_sql_query(delete_timetable_query, delete_timetable_params)

    message = {'message' : "삭제 성공"}

    return JsonResponse(message, safe=False)
