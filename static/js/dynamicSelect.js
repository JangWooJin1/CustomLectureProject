$(document).ready(function () {
    $("#curriculumSelect").change(function () {
        var selectedValue = $(this).val();

        // AJAX 요청으로 선택에 맞는 옵션들을 가져옵니다.
        $.ajax({
            url: get_classification_options_url,  // Django URL 설정에 따라 수정
            data: { selected_value: selectedValue },
            success: function (data) {
                var classificationSelect = $("#classificationSelect");
                classificationSelect.empty(); // 기존 옵션을 모두 지웁니다.
                classificationSelect.append(new Option("--전체--", "all"));

                // 받아온 데이터를 기반으로 새로운 옵션을 추가합니다.
                for (var i = 0; i < data.length; i++) {
                    classificationSelect.append(new Option(data[i].lecture_classification, data[i].lecture_classification));
                }
            }
        });

        // '전공'이 선택되면 새로운 <select> 태그를 생성하여 옵션들을 AJAX 요청으로 가져옴
        if (selectedValue === '전공') {
            $.ajax({
                url: get_univ_options_url,  // Django URL 설정에 따라 수정
                success: function (data) {
                    var univSelect = $('<select>');
                    univSelect.attr('id', 'univSelect');  // 새로운 <select> 태그의 id 설정
                    univSelect.append(new Option("--선택--", "all"));
                    // 받아온 데이터를 기반으로 새로운 옵션을 추가
                    for (var i = 0; i < data.length; i++) {
                        univSelect.append(new Option(data[i].lecture_univ, data[i].lecture_univ));
                    }

                    // 생성한 <select> 태그를 원하는 위치에 추가
                    var univLabel = $('<label id="univSelectLabel" for="univSelect">대학교</label>');
                    $('#selectContainer').append(univLabel);
                    $('#selectContainer').append(univSelect);

                    var majorSelect = $('<select>');
                    majorSelect.attr('id', 'majorSelect');  // 새로운 <select> 태그의 id 설정
                    majorSelect.append(new Option("--전체--", "all"));

                    var majorLabel = $('<label id="majorSelectLabel" for="majorSelect">전공</label>');
                    $('#selectContainer').append(majorLabel);
                    $('#selectContainer').append(majorSelect);
                }
            });
        } else {
            // '전공'이 아니면 생성한 <select> 태그를 제거
            $('#univSelectLabel').remove();
            $('#majorSelectLabel').remove();
            $('#univSelect').remove();
            $('#majorSelect').remove();
        }
    });

    $(document).on('change', '#univSelect', function () {
        var selectedValue = $(this).val();
        $.ajax({
            url: get_major_options_url,  // Django URL 설정에 따라 수정
            data: { selected_value: selectedValue },
            success: function (data) {
                var majorSelect = $("#majorSelect");
                majorSelect.empty(); // 기존 옵션을 모두 지웁니다.
                majorSelect.append(new Option("--전체--", "all"));

                // 받아온 데이터를 기반으로 새로운 옵션을 추가합니다.
                for (var i = 0; i < data.length; i++) {
                    majorSelect.append(new Option(data[i].lecture_major, data[i].lecture_major));
                }
            }
        });
    });
});