

$(document).ready(function() {

  /* Navigation drop down function */
  $('.icon').click(function() {

     $('nav').toggleClass('active')

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

  // Function to remove flash message
  $('.close').click(function() {

    $('.message').hide();

  });

});
