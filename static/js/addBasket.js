// '추가' 버튼 클릭 이벤트 핸들러
$(document).on('click', '.add-button', function () {
    // 해당 버튼의 data-lecture-code 속성을 가져옴
    var lectureCode = $(this).data('lecture-code');

    // lectureCode를 사용하여 Ajax 요청 보내기 (예시)
    $.ajax({
        url: add_userbasket_url, // 적절한 URL로 변경해야 함
        type: 'POST',
        data: {
            lecture_code: lectureCode,
        },
        success: function(lectures) {
                console.log("Received data:", lectures);

                // JSON 데이터를 JavaScript 객체로 파싱
                //var lectures = JSON.parse(data);

                //lectures = data;

                // 기존 테이블 내용을 지우기
                $('#UserBasketTable').empty();

                // 테이블 행을 생성하고 데이터를 추가
                var tableRows = '<tr><th>교과과정</th><th>교과영역구분</th><th>학수강좌번호</th><th>강의 이름</th><th>담당 교수</th><th>학점</th></tr>';

                for (var i = 0; i < lectures.length; i++) {
                    var lecture = lectures[i];
                    tableRows += '<tr>';
                    tableRows += '<td>' + lecture.lecture_curriculum + '</td>';
                    tableRows += '<td>' + lecture.lecture_classification + '</td>';
                    tableRows += '<td>' + lecture.lecture_code + '_' + lecture.lecture_number + '</td>';
                    tableRows += '<td>' + lecture.lecture_name + '</td>';
                    tableRows += '<td>' + lecture.lecture_professor + '</td>';
                    tableRows += '<td>' + lecture.lecture_credit + '</td>';
                    tableRows += '</tr>';
                }

                // 생성한 행을 테이블에 추가
                $('#UserBasketTable').append(tableRows);
        },
        error: function(error) {
            // Ajax 요청 실패 시 처리
            console.error('강의 추가 요청 실패', error);
            // 실패한 경우 사용자에게 알림 등을 표시하는 등의 작업 수행
        }
    });
});
