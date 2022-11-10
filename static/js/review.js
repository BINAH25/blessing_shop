$(document).ready(function () {
  

  $(".review-slider").owlCarousel({
    loop: true,
    center: true,
    autoplay: true,
    nav: false,
    dots: false,
    responsive: {
      0: {
        items: 1,
      },
      750: {
        items: 2,
      },
      1200: {
        items: 3,
      },
    },
  });
});
