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
          cars_searched += `<div class="col-lg-6 col-md-4 col-sm-6">
                <div class="courses-thumb courses-thumb-secondary">
                     <div class="courses-top">
                          <div class="courses-image" style="height: 250px;overflow: hidden;">
                               <img src="${data[i].photo}" class="img-responsive" alt="${data[i].make}" style="height: 100%;width: auto;display: block;">
                          </div>
                          <div class="courses-date">
                               <span title="Author"><i class="fa fa-dashboard"></i> ${data[i].mileage}</span>
                               <span title="Author"><i class="fa fa-cube"></i> ${data[i].engine_size}cc</span>
                               <span title="Views"><i class="fa fa-cog"></i> ${data[i].gearbox}</span>
                          </div>
                     </div>

                     <div class="courses-detail">
                          <h3><a href="#">${data[i].description}</a></h3>

                          <p class="lead"><strong>Ksh ${data[i].price}</strong></p>

                          <p>${data[i].fuel} &nbsp;&nbsp;/&nbsp;&nbsp; ${data[i].mfg_year} &nbsp;&nbsp;/&nbsp;&nbsp; ${data[i].condition}</p>
                     </div>

                     <div class="courses-info">
                          <a href="/car_details${data[i].id}/full_carSale_details" class="section-btn btn btn-primary btn-block">View More</a>
                     </div>
                </div>
          </div>`
        }

    cars_div.html(cars_searched)
})})

function dropDownSelection(){
  let car_condition = $("#carCondition").val()
  let car_make = $("#carMake").val()
  let car_model = $("#carModel").val()
  let car_fuel = $("#carFuel").val()
  let car_seats = $("#carSeats").val()
  let car_price = $("#carPrice").val()
  let car_mileage = $("#carMileage").val()
  let car_engine_size = $("#carEngineSize").val()
  console.log(car_condition, car_make, car_model, car_fuel, car_seats, car_price)
  var obj = {}
  if (car_condition != ''){
    Object.assign(obj,{"condition":car_condition})
  }
  if (car_seats != ''){
    Object.assign(obj,{"seats":car_seats})
  }
   if (car_price != ''){
    Object.assign(obj,{"price":car_price})
  }
  if (car_make != ''){
    Object.assign(obj,{"make":car_make})
  }
  if (car_model != ''){
    Object.assign(obj,{"model":car_model})
  }
  if (car_fuel != ''){
    Object.assign(obj,{"fuel":car_fuel})
  }
  if (car_mileage != ''){
    Object.assign(obj,{"mileage":car_mileage})
  }
  if (car_engine_size != ''){
    Object.assign(obj,{"engine_size":car_engine_size})
  }
  console.log(JSON.stringify(obj))
  let cars_div = $("#cars_results")
  cars_div.html("")
  getData(`http://${window.location.hostname}:5000/dropdown_search`,"POST",obj,(data)=> {
    let cars_selected = "";
    if (data.length == 0){
      cars_selected = "<div class='text-center'><h2> There are no cars with these specifications </h2></div>"
    }
        for (let i = 0; i < data.length; i++) {
          cars_selected += `<div class="col-lg-6 col-md-4 col-sm-6">
                <div class="courses-thumb courses-thumb-secondary">
                     <div class="courses-top">
                          <div class="courses-image" style="height: 250px;overflow: hidden;">
                               <img src="${data[i].photo}" class="img-responsive" alt="${data[i].make}"
                               style="height: 100%;width: auto;display: block;">
                          </div>
                          <div class="courses-date">
                               <span title="Author"><i class="fa fa-dashboard"></i> ${data[i].mileage.toLocaleString()}</span>
                               <span title="Author"><i class="fa fa-cube"></i> ${data[i].engine_size.toLocaleString()} CC</span>
                               <span title="Views"><i class="fa fa-cog"></i> ${data[i].gearbox}</span>
                          </div>
                     </div>

                     <div class="courses-detail">
                          <h3><a href="#">${data[i].description}</a></h3>
                            
                          <p class="lead"><strong>Ksh ${data[i].price.toLocaleString()}</strong></p>

                          <p>${data[i].make} &nbsp;&nbsp;/&nbsp;&nbsp; ${data[i].model} &nbsp;&nbsp;/&nbsp;&nbsp; ${data[i].fuel} &nbsp;&nbsp;/&nbsp;&nbsp; ${data[i].mfg_year} &nbsp;&nbsp;/&nbsp;&nbsp; ${data[i].condition}</p>
                     </div>

                     <div class="courses-info">
                          <a href="/car_details${data[i].id}/full_carSale_details" class="section-btn btn btn-primary btn-block">View More</a>
                     </div>
                </div>
          </div>`
        }

    cars_div.html(cars_selected)
})}
$("#carCondition").on("input",(e)=> {
dropDownSelection()
})

$("#carSeats").on("input",(e)=> {
dropDownSelection()
})

$("#carMake").on("input",(e)=> {
dropDownSelection()
})
$("#carModel").on("input",(e)=> {
dropDownSelection()
})

$("#carFuel").on("input",(e)=> {
dropDownSelection()
})

$("#carPrice").on("input",(e)=> {
dropDownSelection()
})

$("#carMileage").on("input",(e)=> {
dropDownSelection()
})

$("#carEngineSize").on("input",(e)=> {
dropDownSelection()
})


const sendEmail = () => {
    console.log("Am called")
    let email = document.getElementById("email").value
    let phone = document.getElementById("phone").value
    let message = document.getElementById("message").value
    getData(`http://127.0.0.1:5000/contact_us`, "POST", {
        "email": email,
        "phone": phone,
        "message": message

    }, (data) => {
        console.log(data)
    })

}

function hireDropDown(){
  let car_rate = $("#carRate").val()
  let car_hire_model = $("#carHireModel").val()
  let car_hire_brand = $("#carBrand").val()
  let car_hire_seats = $("#carHireSeats").val()
  let car_hire_fuel = $("#carHireFuel").val()

  console.log(car_rate)
  var obj = {}
  if (car_rate != ''){
    Object.assign(obj,{"daily_rate":car_rate})
  }
  if (car_hire_brand != ''){
    Object.assign(obj,{"brand":car_hire_brand})
  }
  if (car_hire_fuel != ''){
    Object.assign(obj,{"fuel":car_hire_fuel})
  }
  if (car_hire_seats != ''){
    Object.assign(obj,{"seats":car_hire_seats})
  }
  if (car_hire_model != ''){
    Object.assign(obj,{"model":car_hire_model})
  }
  console.log(JSON.stringify(obj))
  let cars_div = $("#cars_hire_results")
  cars_div.html("")
  getData(`http://${window.location.hostname}:5000/car_hire_search`,"POST",obj,(data)=> {
    let cars_selected = "";
    if (data.length == 0){
      cars_selected = "<div class='text-center'><h2> There are no cars with these specifications </h2></div>"
    }
        for (let i = 0; i < data.length; i++) {
          cars_selected += `<div class="col-lg-6 col-md-4 col-sm-6">
                <div class="courses-thumb courses-thumb-secondary">
                     <div class="courses-top">
                          <div class="courses-image" style="height: 250px;overflow: hidden;">
                               <img src="${data[i].photo}" class="img-responsive" alt="${data[i].brand}"
                               style="height: 100%;width: auto;display: block;">
                          </div>
                          <div class="courses-date">
                               <span title="Author"><i class="fa fa-dashboard"></i> ${data[i].model}</span>
                               <span title="Author"><i class="fa fa-cube"></i> ${data[i].fuel.toLocaleString()}</span>
                               <span title="Views"><i class="fa fa-cog"></i> ${data[i].gearbox}</span>
                          </div>
                     </div>

                     <div class="courses-detail">
                          <h3><a href="#">${data[i].description}</a></h3>
                            
                          <p class="lead"><strong>Ksh ${data[i].daily_rate.toLocaleString()}</strong></p>
                     </div>

                     <div class="courses-info">
                          <a href="/${data[i].id}/full_carHire_details" class="section-btn btn btn-primary btn-block">View More</a>
                     </div>
                </div>
          </div>`
        }

    cars_div.html(cars_selected)
})}
$("#carRate").on("input",(e)=> {
hireDropDown()
})

$("#carHireModel").on("input",(e)=> {
hireDropDown()
})

$("#carHireFuel").on("input",(e)=> {
hireDropDown()
})

$("#carHireSeats").on("input",(e)=> {
hireDropDown()
})
$("#carBrand").on("input",(e)=> {
hireDropDown()
})


var slideIndex = 0;
    showSlides(slideIndex);

    function plusSlides(n) {
      showSlides(slideIndex += n);
    }

    function showSlides(n) {
      var slides = document.getElementsByClassName("mySlides");

      if (n >= slides.length) {
        slideIndex = 0;
      }

      if (n < 0) {
        slideIndex = slides.length - 1;
      }

      for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }

      slides[slideIndex].style.display = "block";
    }
