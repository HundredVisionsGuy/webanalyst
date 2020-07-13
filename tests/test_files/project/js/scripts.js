
$(function(){
  /* Menu Toggle */
  $("#menu-toggle").on("click", function(){
    $(this).toggleClass("opened closed", 500);
    $("nav.primary-nav").toggleClass("closed opened");
    $("article.page").toggleClass("up down");
  });

  /* Image gallery image toggle */
  $('.image-gallery figure').on("click", function(){
    // toggle the 'hidden' class on the display-box
    $(this).find(".display-box").toggleClass("hidden");
  });

  /* image toggle close box */
  $('.image-gallery .close-box').on("click", function(){
    $(this).siblings().toggleClass("hidden");
  });

});
