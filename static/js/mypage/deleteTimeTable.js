$(document).ready(function () {
    $('#delete_timetable').click( function() {
        var class_num = $(this).data('class-num');

        $.ajax ({
            url: delete_timetable_url,
            method: 'GET',
            data: {
                'class_num' : class_num
            },
            success: function(data){
                var timetable_info = $(`#timetable-${class_num}`);
                timetable_info.empty();

                var tableBox = $('.table-container');
                tableBox.find('.detail-lecture').remove();

                var table = $('#detail-table');
                table.empty();

                alert('삭제되었습니다.');
            },
            error: function(error) {
                console.log("시간표 삭제 실패 : "+error);
            }

        });
    });
});