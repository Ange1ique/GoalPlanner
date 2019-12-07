$(function () {

  /* Functions */

  $(window).on('resize', function mobileViewUpdate() {
    var viewportWidth = $(window).width();
    if (viewportWidth < 600) {
      $(".btn").addClass("btn-sm");
      $(".form-control").addClass("form-control-sm");
      $(".container").addClass("p-1");
    }
    else {
      $(".btn").removeClass("btn-sm");
      $(".form-control").removeClass("form-control-sm");
      $(".container").removeClass("p-1");
    }
  }).resize();

});
