function lecture_day_to_px(lecture_day) {
            switch (lecture_day) {
                case '월':
                    return 0;
                case '화':
                    return 20;
                case '수':
                    return 40;
                case '목':
                    return 60;
                case '금':
                    return 80;
                default:
                    return 0;
            }
        }

/* 강의의 시작과 종료 시간을 기준으로 너비 계산 함수 */
function lecture_duration(start_time, end_time) {
    return end_time - start_time;
}
// 랜덤 색상을 저장할 객체
const lectureColors = {};

// 랜덤 색상을 생성하는 함수
function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

$(document).ready(function () {
    $("#submitButton").click(function () {
        $.ajax({
            url: get_lecture_combinations,  // 실제 URL로 교체
            method: "GET",  // 필요에 따라 요청 메서드 수정
            success: function (combinations) {
                // 기존 시간표 내용을 지웁니다
                $(".TimeTableBox").empty();

                for (let i = 0; i < combinations.length; i++) {
                    const lectures = combinations[i];

                    // timetable을 jQuery 객체로 만듭니다
                    const timetable = $("<div>", {
                        class: "timetable"
                    });
                    $(".TimeTableBox").append(timetable);

                    for (let j = 0; j < lectures.length; j++) {
                        const lecture = lectures[j];

                        // lecture_id에 대한 색상 확인 또는 할당
                        let lectureColor = lectureColors[lecture.lecture_id];
                        if (!lectureColor) {
                            // 색상이 없으면 랜덤 색상 할당
                            lectureColor = getRandomColor();
                            // 할당된 색상 저장
                            lectureColors[lecture.lecture_id] = lectureColor;
                        }

                        const lectureDiv = $("<div>", {
                            class: "lecture",
                            style: `
                            top: ${lecture.lecture_start_time * 10}px;
                            left: ${lecture_day_to_px(lecture.lecture_day)}px;
                            height: ${lecture_duration(lecture.lecture_start_time, lecture.lecture_end_time) * 10}px;
                            background-color: ${lectureColor};`, // 저장된 색상 사용
                        });

                        timetable.append(lectureDiv);
                    }
                }
            }
        });
    });
});
