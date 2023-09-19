$(document).ready( function() {
    $('#submitButton').click(function() {
        var day = $('#select-day').val();
        var start_time = $('.range-left').val();
        var end_time = $('.range-right').val();
        var building = $('#select-building').val();

        $.ajax({
            url: get_empty_rooms_url,
            method: 'POST',
            data:{
            },
            success: function(data){
                'day' : day,
                'start_time' : start_time,
                'end_time': end_time,
                'building': building
            },
            error: function(error){
                console.log('빈강의실 조회 실패 : '+ error);
            }

        });

    });
});