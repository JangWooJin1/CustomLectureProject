// '추가' 버튼 클릭 이벤트 핸들러
$('.lectureBox').on('click', '.add-button', function () {
    // 해당 버튼의 data-lecture-code 속성을 가져옴
    var lectureCode = $(this).data('lecture-code');
    var lectureNumber = $(this).data('lecture-number');

    // lectureCode를 사용하여 Ajax 요청 보내기 (예시)
    $.ajax({
        url: add_userbasket_url, // 적절한 URL로 변경해야 함
        type: 'POST',
        data: {
            lecture_code: lectureCode,
            lecture_number: lectureNumber,
        },
        success: function(data) {
            // 개별 추가의 경우
            if (lectureNumber) {

                //예외) 해당 그룹의 첫 추가인 경우 -> 그룹에 해당하는 것도 같이 추가
                var miniTable = $('#' + lectureCode).find('.mini-table');

                if (miniTable.length === 0) {

                    var tableRows = '<div class="mini-table"  style="display: none;">';  // Use a template engine here
                    tableRows += '<div class="mini-table-row"><div>분반</div><div>시간</div><div>교수</div><div>강의실</div><div>캠퍼스</div><div>비고</div><div>개별추가</div></div>'; // Use a template engine here

                }

                var tableRows = `
                    <div id="basket_${lecture.lecture_code}_${lecture.lecture_number}" class="mini-table-row">
                        <div>${lecture.lecture_number}</div>
                        <div>${lecture.combined_lecture_times}</div>
                        <div>${lecture.lecture_professor}</div>
                        <div>${lecture.combined_lecture_rooms}</div>
                        <div>${lecture.lecture_campus}</div>
                        <div>${lecture.lecture_remark}</div>
                        <div><button class="add-button" data-lecture-code="${lecture.lecture_code}" data-lecture-number="${lecture.lecture_number}">추가</button></div>
                    </div>`;

                $('#' + lectureCode).append(tableRows);
            }
            // 그룹 추가의 경우
            else{
                var tableRows = `
                    <div id="basket_${data[0].lecture_code}_meta" class="table-row lecture_group" data-lecture-code="${data[0].lecture_code}" data-is-folded="true">
                        <div>${data[0].lecture_curriculum}</div>
                        <div>${data[0].lecture_classification}</div>
                        <div>${data[0].lecture_code}</div>
                        <div>${data[0].lecture_name}</div>
                        <div>${data[0].lecture_credit}학점</div>
                        <div><button class="delete-button" data-lecture-code="${data[0].lecture_code}">전체제거</button></div>
                    </div>
                    <div id="basket_${data[0].lecture_code}"></div>`;

                // 생성한 행을 테이블에 추가
                $('#UserBasketTable').append(tableRows);
           }
        },
        error: function(error) {
            // Ajax 요청 실패 시 처리
            console.error('강의 추가 요청 실패', error);
            // 실패한 경우 사용자에게 알림 등을 표시하는 등의 작업 수행
        }
    });
});
