$(document).ready(function () {
  $(".category .btn").click(function () {
    let filter = $(this).attr("data-filter");
    if (filter == "all") {
      $(".category .box").show(400);
    } else {
      $(".category .box")
        .not("." + filter)
        .hide(200);
      $(".category .box")
        .filter("." + filter)
        .show(400);
    }

    $(this).addClass("button-active").siblings().removeClass("button-active");
  });
});
