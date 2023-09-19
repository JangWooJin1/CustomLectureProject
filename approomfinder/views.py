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

class RoomFinder(View):
    template_name = "roomfinderPage.html"

    def get(self, request):
        room_list_query = """
        SELECT DISTINCT lecture_room
        FROM appsearch_lectureItemSchedule
        ORDER BY lecture_room
        """

        room_list = execute_raw_sql_query(room_list_query)

        for room in room_list:
            print("room : ", room['lecture_room'])

        return render(request, self.template_name)

    def POST(self, request):
        pass


@csrf_exempt
def get_empty_rooms(request):
    pass
