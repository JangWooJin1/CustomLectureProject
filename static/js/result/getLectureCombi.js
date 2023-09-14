$(document).ready(function () {
    $("#submitButton").click(function () {
        var campus = $("input[name='campus']:checked").val();

        var time = {};
        // 모든 multi-range 요소를 순회하며 처리합니다.
        $(".time").find(".multi-range").each(function () {
            var checkbox = $(this).find(".multi-range-checkbox");
            var dayLabel = $(this).find(".multi-range-label").text();

            // checkbox가 선택된 경우만 처리합니다.
            if (checkbox.is(":checked")) {
                var startValue = $(this).find(".range-left").val();
                var endValue = $(this).find(".range-right").val();

                // 딕셔너리에 해당 요일과 시간 범위를 저장합니다.
                time[dayLabel] = {
                    "start": parseInt(startValue),
                    "end": parseInt(endValue)
                };
            }
        });

        var credit = {};
        // 모든 multi-range 요소를 순회하며 처리합니다.
        $(".credit").find(".multi-range").each(function () {
            var checkbox = $(this).find(".multi-range-checkbox");
            var keyLabel = $(this).find(".multi-range-label").text();

            // checkbox가 선택된 경우만 처리합니다.
            if (checkbox.is(":checked")) {
                var minValue = $(this).find(".range-left").val();
                var maxValue = $(this).find(".range-right").val();

                credit[keyLabel] = {
                    "min": parseInt(minValue),
                    "max": parseInt(maxValue)
                };
            }
        });

        var group = [];
        $("#selected-groups div").each(function () {
            var id = $(this).attr("id");
            group.push(id);
        });

        $.ajax({
            url: get_lecture_combinations,  // 실제 URL로 교체
            method: "POST",  // 필요에 따라 요청 메서드 수정
            data:{
                'campus' : campus,
                'time' : JSON.stringify(time),
                'credit' : JSON.stringify(credit),
                'group' : JSON.stringify(group),
            },
            success: function (datas) {
                var count_all_combinations = datas.count_all_combinations;

                var count_text = `총 ${count_all_combinations}개 시간표`
                $(".calculateCombination").text(count_text);

                var combinations = datas.valid_combinations;
                // 기존 시간표 내용을 지웁니다
                $(".TimeTableBox").empty();

                var max_end_time = 7.0;

                for (let i = 0; i < combinations.length; i++) {
                    const lectures = combinations[i];

                    // timetable을 jQuery 객체로 만듭니다
                    const timetable = $("<div>", {
                        class: "timetable"
                    });

                    const timetableNum = $("<div>", {
                        class: "timetable-num",
                        text: i + 1
                    });

                    timetable.append(timetableNum);
                    $(".TimeTableBox").append(timetable);


                    max_end_time = 7.0;
                    for (var j = 0; j < lectures.length; j++){
                        var lecture = lectures[j];
                        max_end_time = Math.max(max_end_time, lecture.lecture_end_time);
                    }


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
                            top: ${lecture_time_to_px(lecture.lecture_start_time, max_end_time)}px;
                            left: ${lecture_day_to_px(lecture.lecture_day)}px;
                            height: ${lecture_time_to_height(lecture.lecture_start_time, lecture.lecture_end_time, max_end_time)}px;
                            background-color: ${lectureColor};`, // 저장된 색상 사용
                        "data-lecture-id": lecture.lecture_id,
                        "data-lecture-name": lecture.lecture_name,
                        "data-lecture-professor": lecture.lecture_professor,
                        "data-lecture-room": lecture.lecture_room,
                        "data-lecture-day": lecture.lecture_day,
                        "data-lecture-start-time": lecture.lecture_start_time,
                        "data-lecture-end-time": lecture.lecture_end_time
                    });

                        timetable.append(lectureDiv);
                    }
                }
            }
        });
    });
});

function lecture_day_to_px(lecture_day) {
    var days = ['월', '화', '수', '목', '금'];
    var width = 20;

    return days.indexOf(lecture_day) * width;
}

function lecture_time_to_px(lecture_startTime, max_end_time) {
    var height = 80;
    //0.5 교시 높이 단위
    var height_interval = (height / max_end_time);

    // 시작 시간 차이에 따른 위치 계산
    var positionY = lecture_startTime * height_interval;

    return positionY;
}

function lecture_time_to_height(lecture_startTime, lecture_endTime, max_end_time) {
    var height = 80;
    //0.5 교시 높이 단위
    var height_interval = (height / max_end_time);

    var durationTime = lecture_endTime - lecture_startTime + 0.5; // 수업 기간 (분)

    // 수업 기간에 따른 높이 계산
    var height = durationTime * height_interval;

    return height;
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