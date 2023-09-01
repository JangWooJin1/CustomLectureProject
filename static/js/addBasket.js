// 원하는 이벤트를 강제로 발생시키는 함수
function triggerEvent(element, eventName) {
    var event = new Event(eventName);
    element.dispatchEvent(event);
}

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

                //예외1) 추가하려는 강의의 그룹이 장바구니에 존재x -> 그룹 정보를 장바구니에 추가
                console.log("장바구니 여부 확인 전");
                var basketGroupElement = $(`#basket_${lectureCode}_group`);

                console.log(basketGroupElement);
                if (basketGroupElement.length === 0) {
                    console.log("장바구니 예외 처리 처음");
                    var groupElement = $(`#${lectureCode}_group`);
                    var copyGroupElement = groupElement.clone().prop('id', `basket_${lectureCode}_group`);

                    var copyButton = copyGroupElement.find('.add-button');
                    copyButton
                        .removeClass('add-button')
                        .addClass('delete-button')
                        .text('제거');

                    var detailElement = `<div id="basket_${lectureCode}"></div>`;

                    $('#UserBasketTable').append(copyGroupElement);
                    $('#UserBasketTable').append(detailElement);

                    basketGroupElement = $(`#basket_${lectureCode}_group`);
                    console.log("장바구니 예외 처리 끝")
                }

                //예외2) 해당 그룹의 미니 테이블이 존재하지 않는 경우 -> 미니 테이블을 그룹에 추가
                var miniTableElement = $(`#basket_${lectureCode}`).find('.mini-table');

                if(miniTableElement.length === 0){
                    console.log("미니테이블 예외 처리 전");
                    var basketGroupElement2 = document.querySelector(`#basket_${lectureCode}_group`);
                    triggerEvent(basketGroupElement2, 'click');
                    miniTableElement = $(`#basket_${lectureCode}`).find('.mini-table');
                    console.log("미니테이블 예외 처리 후");
                }

                // 강의조회에서 개별 강의 정보 가져와 반영
                var itemElement = $(`#${lectureCode}_${lectureNumber}_item`);
                var copyItemElement = itemElement.clone().prop('id', `basket_${lectureCode}_${lectureNumber}_item`);

                var copyItemButton = copyItemElement.find('.add-button');
                copyItemButton
                    .removeClass('add-button')
                    .addClass('delete-button')
                    .text('제거');

                miniTableElement.append(copyItemElement);
            }
            // 그룹 추가의 경우
            else{
                var groupElement = $(`#${lectureCode}_group`);
                var copyGroupElement = groupElement.clone().prop('id', `basket_${lectureCode}_group`);

                var copyButton = copyGroupElement.find('.add-button');
                copyButton
                    .removeClass('add-button')
                    .addClass('delete-button')
                    .text('제거');

                var detailElement = `<div id="basket_${lectureCode}"></div>`;

                $('#UserBasketTable').append(copyGroupElement);
                $('#UserBasketTable').append(detailElement);
           }
        },
        error: function(error) {
            // Ajax 요청 실패 시 처리
            console.error('강의 추가 요청 실패', error);
            // 실패한 경우 사용자에게 알림 등을 표시하는 등의 작업 수행
            alert('이미 추가된 강의입니다');
        }
    });
});
