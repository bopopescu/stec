
$(document).ready(function() {

  /* Navigation drop down function in user and admin */
  $('.bars').on('click', function() {

     $('aside').toggle();

  });

  /* Navigation drop down function in user and admin */
  $('.expand').on('click', function() {

     $('aside').hide();
     $('.dashboard').removeClass('dashboard').addClass('extend');

  });


  // Function to remove flash message
  $('.compress').click(function() {

    $('aside').show();
    $('.dashboard').removeClass('extend').addClass('dashboard');

  });

});
