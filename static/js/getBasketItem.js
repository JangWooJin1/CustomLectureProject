$(document).ready(function () {
    $('.basketBox').on('click', '.lecture_group', function () {
        var lectureGroup = $(this);
        var lectureCode = lectureGroup.data('lecture-code');
        var isFolded = lectureGroup.data('is-folded');
        lectureGroup.data('is-folded', !isFolded);
        var miniTable = $('#basket_' + lectureCode).find('.mini-table');

        if (miniTable.length === 0) {
            $.ajax({
                url: get_userbasket_items_url,
                method: "POST",
                data: {
                    lecture_code: lectureCode
                },
                success: function (lectures) {
                    var tableRows = '<div class="mini-table"  style="display: none;">';  // Use a template engine here
                    tableRows += `
                        <div class="mini-table-row">
                            <div class="item_number">분반</div>
                            <div class="item_time">시간</div>
                            <div class="item_professor">교수</div>
                            <div class="item_room">강의실</div>
                            <div class="item_campus">캠퍼스</div>
                            <div class="item_remark">비고</div>
                            <div class="item_button">개별제거</div>
                        </div>`;

                    for (var i = 0; i < lectures.length; i++) {
                        // Generate lecture rows using a template engine
                        var lecture = lectures[i];
                        tableRows += `
                            <div id="basket_${lecture.lecture_code_id}_${lecture.lecture_number}_item" class="mini-table-row">
                                <div class="item_number">${lecture.lecture_number}</div>
                                <div class="item_time">${lecture.combined_lecture_times}</div>
                                <div class="item_professor">${lecture.lecture_professor}</div>
                                <div class="item_room">${lecture.combined_lecture_rooms}</div>
                                <div class="item_campus">${lecture.lecture_campus}</div>
                                <div class="item_remark">${lecture.lecture_remark}</div>
                                <div class="item_button"><button class="delete-button" data-lecture-code="${lecture.lecture_code_id}" data-lecture-number="${lecture.lecture_number}">제거</button></div>
                            </div>`;
                    }

                    tableRows += '</div>';

                    $('#basket_' + lectureCode).append(tableRows);

                    $('#basket_' + lectureCode).find('.mini-table').slideDown();

                }
            });
        }
        else{
            if (isFolded) {
                miniTable.slideDown();   // Reuse the existing data
            } else {
                miniTable.slideUp();  // Hide the mini-table instead of emptying
            }
        }


    });
});
