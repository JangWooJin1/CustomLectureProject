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
            url: get_lecture_group_url,  // 실제 URL로 수정
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
                var tableRows = `
                    <div class="table-row">
                        <div>교과과정</div>
                        <div>교과영역구분</div>
                        <div>학수번호</div>
                        <div>과목명</div>
                        <div>학점</div>
                        <div>그룹추가</div>
                    </div>`;

                for (var i = 0; i < groups.length; i++) {
                    tableRows += `
                        <div class="table-row lecture_group" data-isFolded="true" data-lecture-code="${groups[i].lecture_code}">
                            <div>${groups[i].lecture_curriculum}</div>
                            <div>${groups[i].lecture_classification}</div>
                            <div>${groups[i].lecture_code}</div>
                            <div>${groups[i].lecture_name}</div>
                            <div>${groups[i].lecture_credit}학점</div>
                            <div><button class="add-button" data-lecture-code="${groups[i].lecture_code}">추가</button></div>
                        </div>
                        <div id="${groups[i].lecture_code}"></div>`;
                }

                // 생성한 행을 테이블에 추가
                $('#lectureTable').append(tableRows);
            }
        });
    });
});
