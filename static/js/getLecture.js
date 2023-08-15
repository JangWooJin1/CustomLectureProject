$(document).ready(function () {
    // 조회 버튼 클릭 이벤트 핸들러 등록
    $("#submitButton").click(function () {
        // 선택된 값들 가져오기
        var selectedCurriculum = $("#curriculumSelect").val();
        var selectedClassification = $("#classificationSelect").val();
        var selectedCampus = $("#campusSelect").val();
        var selectedUniv = $("#univSelect").val();
        var selectedMajor = $("#majorSelect").val();

        var selectedSearchCondition = $("#selectSearchConditions").val();
        var searchText = $("#searchText").val();

        // AJAX 요청 보내기
        $.ajax({
            url: get_lecture_url,  // 실제 URL로 수정
            method: "POST",  // 또는 "POST", 요청 방식에 따라 수정
            data: {
                curriculum: selectedCurriculum,
                classification: selectedClassification,
                campus: selectedCampus,
                univ: selectedUniv,
                major: selectedMajor,
                searchCondition : selectedSearchCondition,
                search: searchText
            },
            success: function (groups) {
                // 기존 테이블 내용을 지우기
                $('#lectureTable').empty();


                // 테이블 행을 생성하고 데이터를 추가
                var tableRows = '';
                for(var j=0; j<groups.length; j++){
                    console.log(groups)
                    tableRows += '<details>'
                    tableRows += '<summary>'
                    tableRows += '<td>' + groups[j][0].lecture_curriculum + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_classification + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_code + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_name + '</td> ';
                    tableRows += '<td>' + groups[j][0].lecture_credit + '</td> ';
                    tableRows += '<td><button class="add-button" data-lecture-code="' + groups[j][0].lecture_code + '">전체추가</button></td>';
                    tableRows += '</summary>'
                    var lectures = groups[j];

                    for (var i = 0; i < lectures.length; i++) {
                        var lecture = lectures[i];
                        tableRows += '<td>' + lecture.lecture_number + '</td> ';
                        tableRows += '<td>' + lecture.lecture_professor + '</td> ';
                        tableRows += '<td>' + lecture.lecture_day + '</td> ';
                        tableRows += '<td>' + lecture.lecture_start_time + '</td> ';
                        tableRows += '<td>' + lecture.lecture_end_time + '</td> ';
                        tableRows += '<td><button class="add-button" data-lecture-code="' + lecture.lecture_code + '" data-lecture-number="' + lecture.lecture_number +  '">추가</button></td>';
                        tableRows += '<br>';
                    }
                    tableRows += '</details>'
                }

                // 생성한 행을 테이블에 추가
                $('#lectureTable').append(tableRows);
            }
        });
    });
});
