$(document).ready(function () {
    $(document).on('click', '.lecture_group', function () {
        var lectureCode = $(this).data('lecture-code');
        var isFolded = $(this).data('isFolded');

        var tableRows = ""; // 테이블 행을 저장할 변수 초기화

        if (isFolded) {
            // AJAX 요청 보내기
            $.ajax({
                url: get_lecture_url,
                method: "POST",
                data: {
                    lecture_code: lectureCode
                },
                success: function (lectures) {
                    // 테이블 행 생성
                    tableRows += '<div class="mini-table">';
                    tableRows += '<div class="mini-table-row"><div>분반</div><div>시간</div><div>교수</div><div>강의실</div><div>캠퍼스</div><div>비고</div><div>개별추가</div></div>';

                    for (var i = 0; i < lectures.length; i++) {
                        var lecture = lectures[i];
                        tableRows += `
                            <div class="mini-table-row">
                                <div>${lecture.lecture_number}</div>
                                <div>${lecture.combined_lecture_times}</div>
                                <div>${lecture.lecture_professor}</div>
                                <div>${lecture.combined_lecture_rooms}</div>
                                <div>${lecture.lecture_campus}</div>
                                <div>${lecture.lecture_remark}</div>
                                <div><button class="add-button" data-lecture-code="${lecture.lecture_code}" data-lecture-number="${lecture.lecture_number}">추가</button></div>
                            </div>`;
                    }
                    tableRows += '</div>';

                    // 생성한 행을 해당 강의 그룹 아래에 추가
                    $('#' + lectureCode).append(tableRows);
                }
            });
        } else { // 접혀져 있지 않은 상태인 경우
            // 해당 강의 그룹 아래의 내용을 지우기
            $('#' + lectureCode).empty();
        }

        // 상태를 변경하여 접혀있는지를 추적
        isFolded = !isFolded;
        $(this).data('isFolded', isFolded);
    });
});
