// '추가' 버튼 클릭 이벤트 핸들러
$('.basketBox').on('click', '.delete-button', function () {
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
                var metaDivId = `basket_${lectureCode}_group`;
                var groupDivId = `basket_${lectureCode}`;

                //개별 삭제인 경우
                if(lectureNumber){
                    var itemDivId = `#basket_${lectureCode}_${lectureNumber}_item`;

                    $(itemDivId).remove();

                    //예외) 마지막 남은 강의가 삭제되는 경우 -> 그룹 삭제도 같이
                        if ($(`#${groupDivId} .mini-table`).children().length === 1) {
                            console.log("설마 이거 실행됨?22");
                            $(`#${metaDivId}`).remove();
                            $(`#${groupDivId}`).remove();
                        }
                    console.log("되나3");
                }
                //그룹 삭제인 경우
                else{
                    // 해당 태그를 삭제
                    console.log("설마 이거 실행됨?");
                    $(`#${metaDivId}`).remove();
                    $(`#${groupDivId}`).remove();
                }
        },
        error: function(error) {
            // Ajax 요청 실패 시 처리
            console.error('강의 제거 요청 실패', error);
            // 실패한 경우 사용자에게 알림 등을 표시하는 등의 작업 수행
        }
    });
});
