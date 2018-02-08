$(document).ready(function(){
    swiper1();
    swiper2();
})

function swiper1(){
    var sw1 = new Swiper('#topSwiper', {
         direction: 'horizontal',
         loop: true,
         speed:500,
         autoplay:2000,
         pagination: {
            el: '.swiper-pagination',
         },
    })
}
function swiper2(){
    var sw1 = new Swiper('#menuSwiper', {
        slidesPerView: 3,
        paginationClickable: true,
        spaceBetween: 2,
        loop: false,
    })
}

