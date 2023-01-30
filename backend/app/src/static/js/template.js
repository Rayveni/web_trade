function currency_print(currency_value,currency,locale='ru') {
    let formatter = new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currency,

            // These options are needed to round to whole numbers if that's what you want.
            //minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
            //maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
        });

    return formatter.format(currency_value);
}


function today(add_month=0,str_today="") {
      if (str_today == "") {
          var today_var = new Date()
      } else {
          var today_var = new Date(str_today)
      }
	  
	  today_var.setMonth(today_var.getMonth() + add_month);
	
var dd = String(today_var.getDate()).padStart(2, '0');
var mm = String(today_var.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today_var.getFullYear();

return yyyy  + '-' + mm + '-' + dd;
}

(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });




})(jQuery); // End of use strict



