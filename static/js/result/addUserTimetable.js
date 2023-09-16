$(document).ready(function () {
    $("#addButton").click(function () {
        var table_container = $('.table-container');

        var lectures = [];
        table_container.find('.detail-lecture').each(function (){
            var lecture_id = $(this).data('lecture-id');
            lectures.push(lecture_id);
        });

        $.ajax({
            url: add_user_timetable,
            method: "POST",
            data: {
                'lectures' : JSON.stringify(lectures)
            },
            success: function(data){
                alert('저장이 완료되었습니다.');
            },
            error: function(error){
                console.log('시간표 저장 실패 : '+ error);
            }
        });
   });
});
