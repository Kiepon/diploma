const swiper = new Swiper('.swiper', {
    slidesPerView: 1,
    speed: 400,
    centeredSlides: true,
    preventClicks: true,
    noSwiping: false,
    freeMode: false,
    breakpoints: {
        550: {
            slidesPerView: 2,
        },
        950: {
            slidesPerView: 3,
        },
        1200: {
            slidesPerView: 4,
        },
    }
});