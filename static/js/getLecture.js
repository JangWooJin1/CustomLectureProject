$(document).ready(function () {
    $('.lectureBox').on('click', '.lecture_group', function () {
        var lectureGroup = $(this);
        var lectureCode = lectureGroup.data('lecture-code');
        var isFolded = lectureGroup.data('isFolded');
        var miniTable = $('#' + lectureCode).find('.mini-table');

        if (isFolded) {
            if (miniTable.length === 0) {
                $.ajax({
                    url: get_lecture_url,
                    method: "POST",
                    data: {
                        lecture_code: lectureCode
                    },
                    success: function (lectures) {
                        var tableRows = '<div class="mini-table">';  // Use a template engine here
                        tableRows += '<div class="mini-table-row"><div>분반</div><div>시간</div><div>교수</div><div>강의실</div><div>캠퍼스</div><div>비고</div><div>개별추가</div></div>'; // Use a template engine here

                        for (var i = 0; i < lectures.length; i++) {
                            // Generate lecture rows using a template engine
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

                        $('#' + lectureCode).append(tableRows);
                    }
                });
            } else {
                miniTable.show();  // Reuse the existing data
            }
        } else {
            miniTable.hide();  // Hide the mini-table instead of emptying
        }

        lectureGroup.data('isFolded', !isFolded);
    });
});
