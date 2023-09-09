$(document).ready(function () {
    //강의 추가 함수
    $("#select-group-button").click(function () {
        var selectedGroup = $("#select-group");
        var groupBox = $("#selected-groups");

        var selectedValue = selectedGroup.val();
        var selectedText = selectedGroup.find("option:selected").text();

        var groupElement = `
            <div id="${selectedValue}">
                ${selectedText}
                <button class="remove-group" type="button">-</button>
            </div>
        `;

        groupBox.append(groupElement);
    });

    //강의 제거 함수
    $('#selected-groups').on('click', '.remove-group', function () {
        $(this).parent().remove();
    });
});
