const gap = 16;

const carousel = document.getElementById("carousel"),
  content = document.getElementById("content"),
  next = document.getElementById("next"),
  prev = document.getElementById("prev");

next.addEventListener("click", e => {
  carousel.scrollBy(width + gap, 0);
  if (carousel.scrollWidth !== 0) {
    prev.style.display = "flex";
  }
  if (content.scrollWidth - width - gap <= carousel.scrollLeft + width) {
    next.style.display = "none";
  }
});
prev.addEventListener("click", e => {
  carousel.scrollBy(-(width + gap), 0);
  if (carousel.scrollLeft - width - gap <= 0) {
    prev.style.display = "none";
  }
  if (!content.scrollWidth - width - gap <= carousel.scrollLeft + width) {
    next.style.display = "flex";
  }
});

let width = carousel.offsetWidth;
window.addEventListener("resize", e => (width = carousel.offsetWidth));


var testimonialItems = document.querySelectorAll(".item-slider label");
var timer;
function cycleTestimonials(index) {
   timer = setTimeout(function() {
    var evt;
    if (document.createEvent){
      //If browser = IE, then polyfill
      evt = document.createEvent('MouseEvent');
      evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    } else {
      evt = new MouseEvent("click", {
            view: window,
            bubbles: true,
            cancelable: true,
            clientX: 20
          });
    }
    var ele = "." + testimonialItems[index].className;
    var ele2 = document.querySelector(ele)
    ele2.dispatchEvent(evt);
    index++;
    if (index >= testimonialItems.length) {
      index = 0;
    }
    cycleTestimonials(index);
    document.querySelector(".testimonials").addEventListener("click", function() {
      clearTimeout(timer);
    });
  }, 5000);
}
//run the function
cycleTestimonials(0);


document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('hotel-form');
  const preloader = document.getElementById('preloader');

  const formUrl = form.getAttribute('data-url');

  form.addEventListener('submit', function (event) {
      event.preventDefault();
      preloader.style.display = 'flex';

      const formData = new FormData(form);
      const searchUrl = form.getAttribute('data-search-url');

      const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

      fetch(formUrl, {
          method: 'POST',
          body: formData,
          headers: {
              'X-CSRFToken': csrfToken
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              window.location.href = searchUrl;
          } else {
              alert('Произошла ошибка при обработке запроса.');
          }
      })
      .catch(error => {
          console.error('Ошибка:', error);
          alert('Произошла ошибка при отправке данных.');
      })
  });
});