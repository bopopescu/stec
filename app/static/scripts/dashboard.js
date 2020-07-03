
$(document).ready(function() {

  /* Navigation drop down function in user and admin */
  $('.bars').on('click', function() {

     $('aside').toggle();

  });

  // Function to show aside in large screen
  $('.compress').click(function() {

    $('aside').show();
    $('.extend').removeClass('extend').addClass('dashboard');

  });

  // Function to hide aside in large screen
  $('.expand').on('click', function() {

     $('aside').hide();
    $('.dashboard').removeClass('dashboard').addClass('extend');

  });

  // Function to add active class to Navigation
  $('.links').click(function () {
    $('.links.active').removeClass('active');
    $(this).addClass('active');
  });


});
