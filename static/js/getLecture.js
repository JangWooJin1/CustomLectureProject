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
            success: function (data) {
                // JSON 데이터를 JavaScript 객체로 파싱
                var lectures = JSON.parse(data);

                // 기존 테이블 내용을 지우기
                $('#lectureTable').empty();

                // 테이블 행을 생성하고 데이터를 추가
                var tableRows = '<tr><th>교과과정</th><th>교과영역구분</th><th>학수강좌번호</th><th>강의 이름</th><th>담당 교수</th><th>학점</th></tr>';

                for (var i = 0; i < lectures.length; i++) {
                    var lecture = lectures[i].fields;
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
                $('#lectureTable').append(tableRows);
            }
        });
    });
});
