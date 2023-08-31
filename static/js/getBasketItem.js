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
                    tableRows += '<div class="mini-table-row"><div>분반</div><div>시간</div><div>교수</div><div>강의실</div><div>캠퍼스</div><div>비고</div><div>개별추가</div></div>'; // Use a template engine here

                    for (var i = 0; i < lectures.length; i++) {
                        // Generate lecture rows using a template engine
                        var lecture = lectures[i];
                        tableRows += `
                            <div id="basket_${lecture.lecture_code}_${lecture.lecture_number}" class="mini-table-row">
                                <div>${lecture.lecture_number}</div>
                                <div>${lecture.combined_lecture_times}</div>
                                <div>${lecture.lecture_professor}</div>
                                <div>${lecture.combined_lecture_rooms}</div>
                                <div>${lecture.lecture_campus}</div>
                                <div>${lecture.lecture_remark}</div>
                                <div><button class="delete-button" data-lecture-code="${lecture.lecture_code}" data-lecture-number="${lecture.lecture_number}">제거</button></div>
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
