(function ($) {

  "use strict";

    // PRE LOADER
    $(window).load(function(){
      $('.preloader').fadeOut(1000); // set duration in brackets    
    });


    // MENU
    $('.navbar-collapse a').on('click',function(){
      $(".navbar-collapse").collapse('hide');
    });

    $(window).scroll(function() {
      if ($(".navbar").offset().top > 50) {
        $(".navbar-fixed-top").addClass("top-nav-collapse");
          } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
          }
    });


    // HOME SLIDER & COURSES & CLIENTS
    $('.home-slider').owlCarousel({
      animateOut: 'fadeOut',
      items:1,
      loop:true,
      dots:false,
      autoplayHoverPause: false,
      autoplay: true,
      smartSpeed: 1000,
    })

    $('.owl-courses').owlCarousel({
      animateOut: 'fadeOut',
      loop: true,
      autoplayHoverPause: false,
      autoplay: false,
      dots: false,
      nav:true,
      navText: [
          '<i class="fa fa-angle-left"></i>',
          '<i class="fa fa-angle-right"></i>'
      ],
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        1000: {
          items: 3,
        }
      }
    });

    $('.owl-client').owlCarousel({
      animateOut: 'fadeOut',
      loop: true,
      autoplayHoverPause: false,
      autoplay: true,
      smartSpeed: 1000,
      responsiveClass: true,
      responsive: {
        0: {
          items: 1,
        },
        1000: {
          items: 3,
        }
      }
    });


    // SMOOTHSCROLL
    $(function() {
      $('.custom-navbar a, #home a').on('click', function(event) {
        var $anchor = $(this);
          $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top - 49
          }, 1000);
            event.preventDefault();
      });
    });  

})(jQuery);

const getData = (url,methods,data,handle) => {
   fetch(url,{
     method: methods,
     headers: {
       'Accept': 'application/json',
       'Content-Type': 'application/json'
     },
     body: JSON.stringify(data)
   })
   .then(res=>res.json())
   .then(res => handle(res));
  };
$("#searchBox").on("input",(e)=>{
   let search_term = $("#searchBox").val()
    let cars_div = $("#cars_results")
    cars_div.html("")
    getData(`http://${window.location.hostname}:5000/livesearch`,"POST",{"text" : search_term},(data)=>{
    let cars_searched = "";
        for (let i = 0; i < data.length; i++) {
            cars_searched+= `<div class="col-sm">
                  <div class="card">
                      <img class="card-img-top img-thumbnail" src="${data[i].photo}">
                      <div class="card-body">
                        <h5 class="card-title">Type: ${data[i].name}<h6 class="card-text">Price: ${data[i].price}
                        <span class="dot"></span>Mileage: ${data[i].mileage}</h6></h5>
                        <a href="#" class="btn btn-primary">Learn More</a>
                      </div>
                  </div>
            </div>`

        }
    cars_div.html(cars_searched)
})})
