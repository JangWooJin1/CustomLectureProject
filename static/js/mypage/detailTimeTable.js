$(document).ready(function () {
    $('.filter-section').on('click', '.timetable_info', function () {
        // 클릭한 .timetable 요소 내부의 모든 .lecture 요소를 선택
        var lectureElements = $(this).find('.timetable > .lecture');

        var tableBox = $('.table-container');
        tableBox.find('.detail-lecture').remove();
        var table = $('#detail-table');

        // 초기값 설정
        var minStartTime = Infinity; // 매우 큰 값으로 초기화
        var maxEndTime = -Infinity;  // 매우 작은 값으로 초기화

        // 각 .lecture 요소를 순회하면서 데이터 속성 값을 추출하여 변수에 저장
        lectureElements.each(function () {
            var lecture_startTime = parseFloat($(this).data('lecture-start-time'));
            var lecture_endTime = parseFloat($(this).data('lecture-end-time'));

            // 최소 시작 시간과 최대 종료 시간 업데이트
            minStartTime = Math.min(minStartTime, lecture_startTime);
            maxEndTime = Math.max(maxEndTime, lecture_endTime);
        });

        var [startMinutes, endMinutes] = calculateMinutes(convertStartTime(minStartTime), convertEndTime(maxEndTime));

        // 테이블을 생성할 시간 범위 설정
        var table_startTime = (startMinutes < 540) ? 480 : 540; // 540 분 = 09:00
        var table_endTime = endMinutes;

        // 테이블 생성
        table.empty(); // 기존 테이블 내용 제거

        var table_head = `
        <tr class="row-first">
            <th class="column-first"></th>
            <th>월</th>
            <th>화</th>
            <th>수</th>
            <th>목</th>
            <th>금</th>
        </tr>
        `
        table.append(table_head);

        while (table_startTime <= table_endTime) {
          var row = $('<tr></tr>');
          var hour = Math.floor(table_startTime / 60);

          var th = $('<th class="column-first">' + hour + '시</th>');
          row.append(th);

          for (var i = 0; i < 5; i++) {
            var td = $('<td></td>');
            row.append(td);
          }

          table.append(row);

          table_startTime += 60; // 60분 간격으로 테이블 생성
        }

        table_startTime = (startMinutes < 540) ? 480 : 540; // 540 분 = 09:00
        console.log("여기???");
        // 각 .lecture 요소를 순회하면서 데이터 속성 값을 추출하여 변수에 저장
        lectureElements.each(function () {
        console.log("여기??");
            var lectureId = $(this).data('lecture-id');
            console.log("여기??1");
            var lectureName = $(this).data('lecture-name');
            console.log("여기?2");
            var professor = $(this).data('lecture-professor');
            var room = $(this).data('lecture-room');
            var day = $(this).data('lecture-day');
            var lecture_startTime = convertStartTime(parseFloat($(this).data('lecture-start-time')));
            var lecture_endTime = convertEndTime(parseFloat($(this).data('lecture-end-time')));
            var lectureColor = lectureColors[lectureId];
            if (!lectureColor) {
                // 색상이 없으면 랜덤 색상 할당
                lectureColor = getRandomColor();
                // 할당된 색상 저장
                lectureColors[lectureId] = lectureColor;
            }

           console.log("여기??111");
            var [startMinutes, endMinutes] = calculateMinutes(lecture_startTime, lecture_endTime) ;

            var lectureDiv = $("<div>", {
                class: "detail-lecture",
                style: `
                    top: ${detail_lecture_time_to_px(startMinutes, table_startTime)}px;
                    left: ${detail_lecture_day_to_px(day)}px;
                    height: ${detail_lecture_time_to_height(startMinutes, endMinutes)}px;
                    background-color: ${lectureColor};`,
                "data-lecture-id": lectureId
            });
            var nameDiv = `<div class="name">${lectureName}</div>`;
            var roomDiv = `<div class="room">${room}</div>`;
            var professorDiv = `<div class="professor">${professor}</div>`;

            lectureDiv.append(nameDiv);
            lectureDiv.append(roomDiv);
            lectureDiv.append(professorDiv);

            tableBox.append(lectureDiv);
        });


    });
});

function detail_lecture_day_to_px(lecture_day) {
    var days = ['월', '화', '수', '목', '금'];
    var space = 42.5;
    var width = 123;

    return days.indexOf(lecture_day) * width + space;
}

function detail_lecture_time_to_px(lecture_startTime, table_startTime) {
    var space = 30;
    var hourHeight = 60;
    var minuteHeight = hourHeight / 60; // 1분에 해당하는 픽셀 높이
    var startTimeDifference = lecture_startTime - table_startTime; // 시작 시간 차이 (분)

    // 시작 시간 차이에 따른 위치 계산
    var positionY = startTimeDifference * minuteHeight + space;

    return positionY;
}

function detail_lecture_time_to_height(lecture_startTime, lecture_endTime) {
    var hourHeight = 60;
    var minuteHeight = hourHeight / 60; // 1분에 해당하는 픽셀 높이
    var durationMinutes = lecture_endTime - lecture_startTime; // 수업 기간 (분)

    // 수업 기간에 따른 높이 계산
    var height = durationMinutes * minuteHeight;

    return height;
}

function convertStartTime(startHour) {
  if (startHour >= 0.0 && startHour <= 10.0) {
    // 0.0부터 10.0까지의 경우
    const baseHour = 8; // 시작 시간의 기준 시간 (08:00)
    const minutesPerHour = 60;

    // 시작 시간을 분 단위로 계산
    const totalMinutes = (startHour * minutesPerHour) + (baseHour * minutesPerHour);

    // 분을 시간과 분으로 다시 변환
    const hours = Math.floor(totalMinutes / minutesPerHour);
    const minutes = totalMinutes % minutesPerHour;

    // 시작 시간을 시간 형식 (HH:MM)으로 반환
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
  } else if (startHour >= 10.5 && startHour <= 13.0) {
    // 10.5부터 13.0까지의 경우 특수한 값에 대한 매핑
    const specialTimes = {
      10.5: '18:25',
      11.0: '18:50',
      11.5: '19:15',
      12.0: '19:40',
      12.5: '20:05',
      13.0: '20:40'
    };

    return specialTimes[startHour];
  } else {
    return "Invalid startHour";
  }
}

function convertEndTime(endHour) {
  if (endHour >= 0.0 && endHour <= 9.5) {
    // 0.0부터 9.5까지의 경우
    const baseHour = 8; // 시작 시간의 기준 시간 (08:00)
    const minutesPerHour = 60;

    // 종료 시간을 분 단위로 계산
    const totalMinutes = (endHour * minutesPerHour) + (baseHour * minutesPerHour) + 30; // 30분 추가

    // 분을 시간과 분으로 다시 변환
    const hours = Math.floor(totalMinutes / minutesPerHour);
    const minutes = totalMinutes % minutesPerHour;

    // 종료 시간을 시간 형식 (HH:MM)으로 반환
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
  } else if (endHour >= 10.0) {
    // 10.0 이상부터는 특수한 값에 대한 매핑
    const specialTimes = {
      10.0: '18:25',
      10.5: '18:50',
      11.0: '19:15',
      11.5: '19:40',
      12.0: '20:05',
      12.5: '20:30',
      13.0: '21:05',
      13.5: '21:30',
      14.0: '21:55',
      14.5: '22:20'
    };

    return specialTimes[endHour];
  } else {
    return "Invalid endHour";
  }
}

// 시작 시간과 종료 시간을 분 단위로 계산하는 함수
function calculateMinutes(startTime, endTime) {
    var startTimeParts = startTime.split(":");
    var endTimeParts = endTime.split(":");

    var startMinutes = parseInt(startTimeParts[0]) * 60 + parseInt(startTimeParts[1]);
    var endMinutes = parseInt(endTimeParts[0]) * 60 + parseInt(endTimeParts[1]);

    return [startMinutes, endMinutes];
}

var lectureColors = {};
function getRandomColor() {
    const letters = "0123456789ABCDEF";
    let color = "#";
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

