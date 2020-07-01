
$(document).ready(function() {

  /* Navigation drop down function in user and admin */
  $('.icon').on('click', function() {

     $('.asidenav').toggle();

  });

  // Function to remove flash message
  $('.close').click(function() {

    $('.message').hide();

  });

});
