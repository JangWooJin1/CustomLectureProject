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
