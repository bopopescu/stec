
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

  /* function to toggle user post edit */
  $('.write').on('click', function() {

     $('.writepost').toggle();

  });

  // Function to remove flash message
  $('.close').click(function() {

     $('.message').hide();

  });

  // Function to add active class to aside naviagation
  $(function () {
     setNavigation();
  });

  function setNavigation() {
    var path = window.location.pathname;
    path = path.replace(/\/$/, "");
    path = decodeURIComponent(path);

    $("aside ul li a").each(function () {
       var href = $(this).attr('href');
       if (path.substring(0, href.length) === href) {
           $(this).closest('li').addClass('active');
       }
    });
  }

});
