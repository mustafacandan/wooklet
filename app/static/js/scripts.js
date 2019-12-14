$(window).scroll(function () {
    if ($(window).scrollTop() > 20) {
      $('.navbar').addClass('golgeli-nav');
    } else {
      $('.navbar').removeClass('golgeli-nav');
    }
  }); 