// '추가' 버튼 클릭 이벤트 핸들러
$(document).on('click', '.delete-button', function () {
    // 해당 버튼의 data-lecture-code 속성을 가져옴
    var lectureCode = $(this).data('lecture-code');
    var lectureNumber = $(this).data('lecture-number');

    // lectureCode를 사용하여 Ajax 요청 보내기 (예시)
    $.ajax({
        url: delete_userbasket_url, // 적절한 URL로 변경해야 함
        type: 'POST',
        data: {
            lecture_code: lectureCode,
            lecture_number: lectureNumber,
        },
        success: function(groups) {

                // 기존 테이블 내용을 지우기
                $('#UserBasketTable').empty();

                // 테이블 행을 생성하고 데이터를 추가
                var tableRows = '';
                for(var j=0; j<groups.length; j++){
                    tableRows += '<details>'
                    tableRows += '<summary>'
                    tableRows += '<td>' + groups[j][0].lecture_curriculum + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_classification + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_code + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_name + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_credit + '</td> ';
                    tableRows += '<td><button class="delete-button" data-lecture-code="' + groups[j][0].lecture_code + '">전체제거</button></td>';
                    tableRows += '</summary>'
                    var lectures = groups[j];

                    for (var i = 0; i < lectures.length; i++) {
                        var lecture = lectures[i];
                        tableRows += '<td>' + lecture.lecture_number + '</td> ';
                        tableRows += '<td>' + lecture.lecture_professor + '</td> ';
                        tableRows += '<td>' + lecture.combined_lecture_times + '</td> ';
                        tableRows += '<td>' + lecture.combined_lecture_rooms + '</td> ';
                        tableRows += '<td><button class="delete-button" data-lecture-code="' + lecture.lecture_code + '" data-lecture-number="' + lecture.lecture_number +  '">제거</button></td>';
                        tableRows += '<br>';
                    }
                    tableRows += '</details>'
                }

                // 생성한 행을 테이블에 추가
                $('#UserBasketTable').append(tableRows);
        },
        error: function(error) {
            // Ajax 요청 실패 시 처리
            console.error('강의 제거 요청 실패', error);
            // 실패한 경우 사용자에게 알림 등을 표시하는 등의 작업 수행
        }
    });
});
