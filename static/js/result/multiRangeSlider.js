// 함수를 하나로 통합하여 코드 중복을 줄입니다.
function initializeMultiRangeSlider(sliderId) {
  const slider = document.getElementById(sliderId);
  const inputLeft = slider.querySelector(".multi-range-slider > .range-left");
  const inputRight = slider.querySelector(".multi-range-slider > .range-right");
  const thumbLeft = slider.querySelector(".slider > .thumb.left");
  const thumbRight = slider.querySelector(".slider > .thumb.right");
  const range = slider.querySelector(".slider > .range");
  const outputLeft = slider.querySelector(".output-value > .output-left");
  const outputRight = slider.querySelector(".output-value > .output-right");

  function updateSlider() {
    const min = parseInt(inputLeft.min);
    const max = parseInt(inputRight.max);
    const leftValue = parseInt(inputLeft.value);
    const rightValue = parseInt(inputRight.value);
    const leftPercent = ((leftValue - min) / (max - min)) * 100;
    const rightPercent = ((rightValue - min) / (max - min)) * 100;

    thumbLeft.style.left = leftPercent + "%";
    thumbRight.style.right = 100 - rightPercent + "%";
    range.style.left = leftPercent + "%";
    range.style.right = 100 - rightPercent + "%";

    outputLeft.textContent = leftValue;
    outputRight.textContent = rightValue;
  }

  inputLeft.addEventListener("input", () => {
    const rightValue = parseInt(inputRight.value);
    inputLeft.value = Math.min(parseInt(inputLeft.value), rightValue - 1);
    updateSlider();
  });

  inputRight.addEventListener("input", () => {
    const leftValue = parseInt(inputLeft.value);
    inputRight.value = Math.max(parseInt(inputRight.value), leftValue + 1);
    updateSlider();
  });

  updateSlider();
}

initializeMultiRangeSlider("slider-1");
initializeMultiRangeSlider("slider-2");
initializeMultiRangeSlider("slider-3");
initializeMultiRangeSlider("slider-4");
initializeMultiRangeSlider("slider-5");
initializeMultiRangeSlider("slider-6");

$(document).ready(function () {
  // 첫 로드시 숨김 처리
  $('.multi-range')
    .find('.range-left, .range-right, .range, .thumb.left, .thumb.right, .output-left, .output-right')
    .hide();

  // 체크박스의 변경 이벤트를 감지합니다.
  $('.multi-range-checkbox').change(function () {
    // 체크박스의 상태를 확인합니다.
    if (!$(this).prop('checked')) {
      // 체크박스가 선택되지 않았을 때, 해당 multi-range 요소를 숨깁니다.
      $(this)
        .closest('.multi-range')
        .find('.range-left, .range-right, .range, .thumb.left, .thumb.right, .output-left, .output-right')
        .hide();
    } else {
      // 체크박스가 선택되었을 때, 해당 multi-range 요소를 표시합니다.
      $(this)
        .closest('.multi-range')
        .find('.range-left, .range-right, .range, .thumb.left, .thumb.right, .output-left, .output-right')
        .show();
    }
  });
});




