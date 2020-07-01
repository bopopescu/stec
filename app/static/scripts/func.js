$(document).ready(function() {

  /* Navigation drop down function in user and admin */
  $('.icon').on('click', function() {

     $('nav').slideToggle();

  });


  // Function to change the nav-bar on scroll
  $(window).on("scroll", function() {

    if($(window).scrollTop()){
      $('nav').addClass('grey');
    }
    else {
      $('nav').removeClass('grey');
    }

  });

});
