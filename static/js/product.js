
//product image animation--------------
$('.prod-img').elevateZoom({
  gallery: "gallery",
  // galleryActiveClass: "activeborder",
  zoomType: "window", //lens, windows, inner
  zoomWindowWidth: 400,
  zoomWindowHeight: 530,
  borderSize: 1,
  borderColour: "#fff",
  cursor: "crosshair",
  easing: "True",
  easingType: "zoomdefault",
  scrollZoom:"True",
  zoomWindowFadeIn: 500,
  zoomWindowFadeOut: 750
});
$(".prod-img").bind("click", function (e) {
  var ez = $('.prod-img').data('elevateZoom');
  ez.closeAll();
  $.fancybox(ez.getGalleryList());
  return false;
});
$('#prod-img1').css({"border" : "5px solid #fff"});
$('#prod-img1').click(function(){
  $(this).css({"border" : "5px solid #fff"});
  $('#prod-img2').css({"border" : "transparent"});
  $('#prod-img3').css({"border" : "transparent"});
});
$('#prod-img2').click(function(){
  $(this).css({"border" : "5px solid #fff"});
  $('#prod-img1').css({"border" : "transparent"});
  $('#prod-img3').css({"border" : "transparent"});
});
$('#prod-img3').click(function(){
  $(this).css({"border" : "5px solid #fff"});
  $('#prod-img1').css({"border" : "transparent"});
  $('#prod-img2').css({"border" : "transparent"});
});


//-------------------------------------



//calender styles and functions-------

var error = 1;

$(function(){
    $( "#calender" ).datepicker({
      inline: true,
      showOtherMonths: true,
      dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      beforeShowDay: nonSaturday,
      minDate:0,
      maxDate:'+2M',
      rangeSelect: true,
      dateFormat: 'DD, d MM, yy',
      altField: '#delivery',
      onSelect: function(){
        error = 0;
        range();
        $('#cart_error').css({"display": "none"});
      },

    });
  });
  function date_display(){
    $('#date_error').css({"display" : "none"});
    $('#dates').css({"display" : "inline"});
    success = 1;
  }

  function dateError(){
    $('#dates').css({"display" : "none"});
    $('#date_error').css({"display" : "inline-block"});
    error = 1;
  }

  function nonSaturday(date){
      var day = date.getDay(), Sunday = 0, Monday = 1, Tuesday = 2, Wednesday = 3, Thursday = 4, Friday = 5, Saturday = 6;
      // var closedDates = [[7, 29, 2009], [8, 25, 2010]];
      var closedDays = [[Saturday]];
      for (var i = 0; i < closedDays.length; i++) {
          if (day == closedDays[i][0]) {
              return [false];
          }

      }
      return [true];
  }
  function range(){
    var date1 = $('#calender').datepicker('getDate');
    var temp_date = $('#calender').datepicker('getDate');
    var today = new Date();
    today.setHours(0);
    today.setMinutes(0);
    today.setSeconds(0);
    var tom = new Date();
    tom.setHours(0);
    tom.setMinutes(0);
    tom.setSeconds(0);
    tom.setDate(tom.getDate()+1);
    if(Date.parse(today) == Date.parse(temp_date) || Date.parse(tom) == Date.parse(temp_date)){
      dateError();
    }else{
      date_display();
      if($('#rental-check1').is(':checked')){
        date1.setDate(date1.getDate()+4);
        var day = date1.getDay();
        if(day == 6){
          date1 = $('#calender').datepicker('getDate');
          date1.setDate(date1.getDate()+5);
        }
      }
      if($('#rental-check2').is(':checked')){
        date1.setDate(date1.getDate()+8);
        var day = date1.getDay();
        if(day == 6){
          date1 = $('#calender').datepicker('getDate');
          date1.setDate(date1.getDate()+9);
        }
      }
      if($('#rental-check3').is(':checked')){
        date1.setDate(date1.getDate()+30);
        var day = date1.getDay();
          if(day == 6){
            date1 = $('#calender').datepicker('getDate');
            date1.setDate(date1.getDate()+31);
          }
      }
      $('.return').val(date1);
      return_date();
    }
  }
  function return_date(){
    var date_val = $('.return').val();
    var d = new Date(date_val);
    var return_date = $.datepicker.formatDate('DD, d MM, yy', d);
    $('.return').val(return_date);
  }


//----------------------------------------------

// setting value of quantity to 1
$('#qty-input').blur(function() {
  if ($(this).val() == "" || $(this).val() == 0) {
    $(this).val('1');
  }
});
// ----------------------------------

// taking price of rent to quatity value
var rent1=$('#rent-price1').text();
//var rent2=$('#rent-price2').text();
//var rent3=$('#rent-price3').text();
$('#qty-price').text(rent1);
// -------------------------------------------

//element determining--------------------

var element = $('input#element_type').val();
if(element == 'Ornament'){
    $('.normal-size').css({"display": "none"});
}else{
    $('.normal-size').css({"display": "block"});
}
//---------------------------------------

//stock determining-------------

var stock_s = $('input#stock-s').val();
var stock_m = $('input#stock-m').val();
var stock_l = $('input#stock-l').val();
var stock_xl = $('input#stock-xl').val();
var stock_xxl = $('input#stock-xxl').val();
var stock_3xl = $('input#stock-3xl').val();
var stock = parseInt($('input#stock').val());
var delivery_date = $('#delivery').val();

$('.select1').on('change', function(){
   var size = $('.select1 option:selected').val();
    if(size == 'S'){
        stock = $('input#stock').val(stock_s);
        stock = parseInt($('input#stock').val());
    }
    if(size == 'M'){
        stock = $('input#stock').val(stock_m);
        stock = parseInt($('input#stock').val());
    }
    if(size == 'L'){
        stock = $('input#stock').val(stock_l);
        stock = parseInt($('input#stock').val());
    }
    if(size == 'XL'){
        stock = $('input#stock').val(stock_xl);
        stock = parseInt($('input#stock').val());
    }
    if(size == 'XXL'){
        stock = $('input#stock').val(stock_xxl);
        stock = parseInt($('input#stock').val());
    }
    if(size == '3XL'){
        stock = $('input#stock').val(stock_3xl);
        stock = parseInt($('input#stock').val());
    }
    if(stock != 0){
        if($('#check2').is(':checked')){
            if(stock <= 15){
                $('#stock-text').css({"display" : "inline"});
            if(stock >= 5){
                $('#quantity-block').css({"display" : "inline"});
                $('#outstock-text').css({"display" : "none"});
                $('#days-cover').css({"display" : "none"});
                $('#calender-cover').css({"display" : "none"});
                if(delivery_date != ''){
                    $('#dates').css({"display" : "inline"});
                }
                $('#cart-btn').css({"display" : "block"});
                $('#wish-btn').css({"display" : "none"});
            }else{
                $('#quantity-block').css({"display" : "none"});
                $('#stock-text').css({"display" : "none"});
                $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
                $('#days-cover').css({"display" : "block"});
                $('#calender-cover').css({"display" : "block"});
                $('#dates').css({"display" : "none"});
                $('#calender').datepicker('setDate', null);
                $('#cart-btn').css({"display" : "none"});
                $('#wish-btn').css({"display" : "block"});

            }
            }else{
                $('#stock-text').css({"display" : "none"});
            }
        }else{
            $('#quantity-block').css({"display" : "inline"});
            $('#outstock-text').css({"display" : "none"});
            $('#days-cover').css({"display" : "none"});
            $('#calender-cover').css({"display" : "none"});
            if(delivery_date != ''){
                $('#dates').css({"display" : "inline"});
            }
            $('#cart-btn').css({"display" : "block"});
            $('#wish-btn').css({"display" : "none"});
            if(stock <= 5){
                $('#stock-text').css({"display" : "inline"});
            }else{
                $('#stock-text').css({"display" : "none"});
            }
        }

    }else{
              $('#quantity-block').css({"display" : "none"});
              $('#stock-text').css({"display" : "none"});
              $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
              $('#days-cover').css({"display" : "block"});
              $('#calender-cover').css({"display" : "block"});
              $('#dates').css({"display" : "none"});
              $('#calender').datepicker('setDate', null);
              $('#cart-btn').css({"display" : "none"});
              $('#wish-btn').css({"display" : "block"});
    };
});

    var size = $('.select1 option:selected').val();
    if(size == 'S'){
        stock = $('input#stock').val(stock_s);
        stock = parseInt($('input#stock').val());
    };
    if(size == 'M'){
        stock = $('input#stock').val(stock_m);
        stock = parseInt($('input#stock').val());
    };
    if(size == 'L'){
        stock = $('input#stock').val(stock_l);
        stock = parseInt($('input#stock').val());
    };
    if(size == 'XL'){
        stock = $('input#stock').val(stock_xl);
        stock = parseInt($('input#stock').val());
    };
    if(size == 'XXL'){
        stock = $('input#stock').val(stock_xxl);
        stock = parseInt($('input#stock').val());
    };
    if(size == '3XL'){
        stock = $('input#stock').val(stock_3xl);
        stock = parseInt($('input#stock').val());
    }

if(stock != 0){
    $('#quantity-block').css({"display" : "inline"});
    $('#outstock-text').css({"display" : "none"});
    $('#days-cover').css({"display" : "none"});
    $('#calender-cover').css({"display" : "none"});
    $('#cart-btn').css({"display" : "block"});
    $('#wish-btn').css({"display" : "none"});
    if(stock <= 5){
        $('#stock-text').css({"display" : "inline"});
    }else{
        $('#stock-text').css({"display" : "none"});
    }
}else{
          $('#quantity-block').css({"display" : "none"});
          $('#stock-text').css({"display" : "none"});
          $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
          $('#days-cover').css({"display" : "block"});
          $('#calender-cover').css({"display" : "block"});
          $('#dates').css({"display" : "none"});
          $('#calender').datepicker('setDate', null);
          $('#cart-btn').css({"display" : "none"});
          $('#wish-btn').css({"display" : "block"});
};


//-----------back-up-size change stock check-------



//====================================================


//-----------------------------

// setting checkbox when clicking on text
$('#check1').prop("checked", true);
$('#item-rent-msg1').css({"display" : "inline"});
$('#rent-price1').css({"display" : "inline"});
$('input#qty-input').val(1);

//$('#check-text1').click(function(){
//  $('#check1').prop("checked", true);
//  $('#check2').prop("checked", false);
//  $('#check3').prop("checked", false);
//  $('#text-hidden').css({"display" : "none"});
//  $('#item-rent-msg2').css({"display" : "none"});
//  $('#item-rent-msg1').css({"display" : "inline"});
//  $('input#qty-input').val(1);
//  $('#rent-price1').css({"display" : "inline"});
//  $('#rent-price2').css({"display" : "none"});
//  $('#rent-price3').css({"display" : "none"});
//  $('#qty-price').text(rent1);
//  $('#stock-text').css({"display" : "none"});
//  $('#rent-check1').css({"display": "block"});
//  $('#rent-check2').css({"display": "block"});
//  $('#rent-check3').css({"display": "none"});
//  $('#rental-check3').prop("checked", false);
//  $('#rental-check1').prop("checked", true);
//  $('#rental-check2').prop("checked", false);
//  $('#cart_error1').css({"display": "none"});
//  $('#cart_error2').css({"display": "none"});
//  $('#calender').datepicker('setDate', null);
//  $('#dates').css({"display" : "none"});
//    error = 1;
//
//  //stock check-------------
//    if(stock != 0){
//        $('#quantity-block').css({"display" : "inline"});
//        $('#outstock-text').css({"display" : "none"});
//        $('#days-cover').css({"display" : "none"});
//        $('#calender-cover').css({"display" : "none"});
//        if(delivery_date != ''){
//            $('#dates').css({"display" : "inline"});
//        }
//        $('#cart-btn').css({"display" : "block"});
//        $('#wish-btn').css({"display" : "none"});
//        if(stock <= 5){
//            $('#stock-text').css({"display" : "inline"});
//        }else{
//            $('#stock-text').css({"display" : "none"});
//        }
//    }else{
//              $('#quantity-block').css({"display" : "none"});
//              $('#stock-text').css({"display" : "none"});
//              $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
//              $('#days-cover').css({"display" : "block"});
//              $('#calender-cover').css({"display" : "block"});
//              $('#dates').css({"display" : "none"});
//              $('#calender').datepicker('setDate', null);
//              $('#cart-btn').css({"display" : "none"});
//              $('#wish-btn').css({"display" : "block"});
//    };
//
//  //------------------------------
//});
//$('#check-text2').click(function(){
//  $('#check2').prop("checked", true);
//  $('#check1').prop("checked", false);
//  $('#check3').prop("checked", false);
//  $('#text-hidden').css({"display" : "inline"});
//  $('#item-rent-msg1').css({"display" : "none"});
//  $('#item-rent-msg2').css({"display" : "inline"});
//  $('input#qty-input').val(5);
//  $('#rent-price1').css({"display" : "none"});
//  $('#rent-price2').css({"display" : "inline"});
//  $('#rent-price3').css({"display" : "none"});
//  $('#qty-price').text(rent2);
//  $('#rent-check1').css({"display": "block"});
//  $('#rent-check2').css({"display": "block"});
//  $('#rent-check3').css({"display": "none"});
//  $('#rental-check3').prop("checked", false);
//  $('#rental-check1').prop("checked", true);
//  $('#rental-check2').prop("checked", false);
//  $('#cart_error1').css({"display": "none"});
//  $('#cart_error2').css({"display": "none"});
//  $('#calender').datepicker('setDate', null);
//  $('#dates').css({"display" : "none"});
//    error = 1;
//
//  //stock check-------------
//    if(stock != 0){
//        if(stock <= 15){
//            $('#stock-text').css({"display" : "inline"});
//            if(stock >= 5){
//                $('#quantity-block').css({"display" : "inline"});
//                $('#outstock-text').css({"display" : "none"});
//                $('#days-cover').css({"display" : "none"});
//                $('#calender-cover').css({"display" : "none"});
//                if(delivery_date != ''){
//                    $('#dates').css({"display" : "inline"});
//                }
//                $('#cart-btn').css({"display" : "block"});
//                $('#wish-btn').css({"display" : "none"});
//            }else{
//                $('#quantity-block').css({"display" : "none"});
//                $('#stock-text').css({"display" : "none"});
//                $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
//                $('#days-cover').css({"display" : "block"});
//                $('#calender-cover').css({"display" : "block"});
//                $('#dates').css({"display" : "none"});
//                $('#calender').datepicker('setDate', null);
//                $('#cart-btn').css({"display" : "none"});
//                $('#wish-btn').css({"display" : "block"});
//
//            }
//        }else{
//            $('#stock-text').css({"display" : "none"});
//        }
//    }else{
//              $('#quantity-block').css({"display" : "none"});
//              $('#stock-text').css({"display" : "none"});
//              $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
//              $('#days-cover').css({"display" : "block"});
//              $('#calender-cover').css({"display" : "block"});
//              $('#dates').css({"display" : "none"});
//              $('#calender').datepicker('setDate', null);
//              $('#cart-btn').css({"display" : "none"});
//              $('#wish-btn').css({"display" : "block"});
//    };
//
//
//  //------------------------------
//});
//$('#check-text3').click(function(){
//  $('#check3').prop("checked", true);
//  $('#check2').prop("checked", false);
//  $('#check1').prop("checked", false);
//  $('#text-hidden').css({"display" : "none"});
//  $('#item-rent-msg2').css({"display" : "none"});
//  $('#item-rent-msg1').css({"display" : "inline"});
//  $('input#qty-input').val(1);
//  $('#rent-price1').css({"display" : "none"});
//  $('#rent-price2').css({"display" : "none"});
//  $('#rent-price3').css({"display" : "inline"});
//  $('#qty-price').text(rent3);
//  $('#stock-text').css({"display" : "none"});
//  $('#rent-check1').css({"display": "none"});
//  $('#rent-check2').css({"display": "none"});
//  $('#rent-check3').css({"display": "block"});
//  $('#rental-check3').prop("checked", true);
//  $('#rental-check1').prop("checked", false);
//  $('#rental-check2').prop("checked", false);
//  $('#cart_error1').css({"display": "none"});
//  $('#cart_error2').css({"display": "none"});
//  $('#calender').datepicker('setDate', null);
//  $('#dates').css({"display" : "none"});
//error = 1;
//  //stock check-------------
//    if(stock != 0){
//        $('#quantity-block').css({"display" : "inline"});
//        $('#outstock-text').css({"display" : "none"});
//        $('#days-cover').css({"display" : "none"});
//        $('#calender-cover').css({"display" : "none"});
//        if(delivery_date != ''){
//            $('#dates').css({"display" : "inline"});
//        }
//        $('#cart-btn').css({"display" : "block"});
//        $('#wish-btn').css({"display" : "none"});
//        if(stock <= 5){
//            $('#stock-text').css({"display" : "inline"});
//        }else{
//            $('#stock-text').css({"display" : "none"});
//        }
//    }else{
//              $('#quantity-block').css({"display" : "none"});
//              $('#stock-text').css({"display" : "none"});
//              $('#outstock-text').css({"display" : "inline", "font-size" : "17px"});
//              $('#days-cover').css({"display" : "block"});
//              $('#calender-cover').css({"display" : "block"});
//              $('#dates').css({"display" : "none"});
//              $('#calender').datepicker('setDate', null);
//              $('#cart-btn').css({"display" : "none"});
//              $('#wish-btn').css({"display" : "block"});
//    };
//
//
//  //------------------------------
//});
var add_success = 0;
var add_price;
$('#rental-check1').prop("checked", true);
$('#rent-check1').click(function(){
  $('#rental-check1').prop("checked", true);
  $('#rental-check2').prop("checked", false);

  //add amount 50% increase

   if(add_success==1){
       var c_price = parseInt($('#qty-price').text());
//       var sub_price = c_price / 2;
       var sub_price_total = c_price - add_price;
       $('#qty-price').text(sub_price_total);
       add_success = 0;
   }

   //===================

  //--renting dates---------
  var date1 = $('#calender').datepicker('getDate');
  date1.setDate(date1.getDate()+4);
  var day = date1.getDay();
  if(day == 6){
    date1 = $('#calender').datepicker('getDate');
    date1.setDate(date1.getDate()+5);
  }
  $('.return').val(date1);
  return_date();

  //--------------------------

});
$('#rent-check2').click(function(){
  $('#rental-check2').prop("checked", true);
  $('#rental-check1').prop("checked", false);

   //add amount 50% increase

   var c_price = parseInt($('#qty-price').text());
   add_price = c_price / 2;
   var add_price_total = c_price + add_price;
   $('#qty-price').text(add_price_total);
   add_success = 1;

   //===================

//--renting dates---------
  var date1 = $('#calender').datepicker('getDate');
  date1.setDate(date1.getDate()+8);
  var day = date1.getDay();
  if(day == 6){
    date1 = $('#calender').datepicker('getDate');
    date1.setDate(date1.getDate()+9);
  }
  $('.return').val(date1);
  return_date();
  //----------------------------------

});


//-----------------------------------------

// quantity increement decreement

$('#plus-btn').on('click', function(){
  var qty = $('input#qty-input').val();
  if($('#check1').is(':checked')){
        if(stock >= 2){
            if(qty==2){
                $('input#qty-input').val(2);
             }else{
                qty++;
                $('input#qty-input').val(qty);
                total1();
             }
        }
  };
//  if($('#check3').is(':checked')){
//    if(stock >= 2){
//      if(qty==2){
//        $('input#qty-input').val(2);
//      }else{
//        qty++;
//        $('input#qty-input').val(qty);
//        total3();
//      }
//    }
//
//
//  };
//  if($('#check2').is(':checked')){
//    if(stock >= 5){
//      if(qty==15){
//        $('input#qty-input').val(15);
//      }else{
//        if(qty == stock){
//          $('input#qty-input').val(qty);
//        }else{
//          qty++;
//          $('input#qty-input').val(qty);
//          total2();
//        }
//
//      }
//    }
//
//  };

});
$('#minus-btn').on('click', function(){
  var qty = $('input#qty-input').val();
  if($('#check1').is(':checked')){
    if(qty==1){
      $('input#qty-input').val(1);
    }else{
      qty--;
      total_minus1();
      $('input#qty-input').val(qty);
    }
  };
//  if($('#check3').is(':checked')){
//    if(qty==1){
//      $('input#qty-input').val(1);
//    }else{
//      qty--;
//      $('input#qty-input').val(qty);
//      total_minus3();
//    }
//  };
//  if($('#check2').is(':checked')){
//    if(qty==5){
//      $('input#qty-input').val(5);
//    }else{
//      qty--;
//      $('input#qty-input').val(qty);
//      total_minus2();
//    }
//  };

});



//function for price calculation

//for personal rent
function total1(){
if(add_success==1){
   var c_price = parseInt($('#qty-price').text());
   var qty = $('input#qty-input').val();
   var add_price_total = c_price * qty;
   $('#qty-price').text(add_price_total);
}else{
    var rent_price1=$('#rent-price1').text();
    var qty = $('input#qty-input').val();
    rent_price1 = rent_price1 * qty;
    $('#qty-price').text(rent_price1);
}

}
function total_minus1(){
if(add_success==1){
   var c_price = parseInt($('#qty-price').text());
   var qty = Number($('input#qty-input').val());
   var sub_price_total_minus = c_price / qty;
   $('#qty-price').text(sub_price_total_minus);
}else{
    var c_price = parseInt($('#qty-price').text());
    var qty = $('input#qty-input').val();
    rent_price1 = c_price / qty;
    $('#qty-price').text(rent_price1);
}

}
//-------------------------

//for event rent----------------

//    function total2(){
//    var rent_price1=parseInt($('#rent-price1').text());
//    var rent_price2=parseInt($('#rent-price2').text());
//    var temp_rent = $('#rent-price2').text();
//    var temp_qty_rent = parseInt($('#qty-price').text());
//    var qty = $('input#qty-input').val();
//    var price=5;
//    var price_count = 13;
//
//    if(qty==10){
//      temp_rent = temp_rent * 2;
//      rent_price2 = Number(temp_rent);
//      $('#qty-price').text(rent_price2);
//    }
//    else if(qty==15){
//      temp_rent = temp_rent * 3;
//      rent_price2 = temp_rent;
//      $('#qty-price').text(rent_price2);
//    }else{
//      do{
//          rent_price2 = rent_price2 + rent_price1;
//          $('#qty-price').text(rent_price2);
//          price++;
//      }while(price<qty);
//    }
//
//    }
//
//    function total_minus2(){
//    var rent_price1=parseInt($('#rent-price1').text());
//    var rent_price2=parseInt($('#rent-price2').text());
//    var temp_rent = $('#rent-price2').text();
//    var temp_qty_rent = parseInt($('#qty-price').text());
//    var qty = $('input#qty-input').val();
//    var price=5;
//
//    if(qty==9){
//      do{
//          rent_price2 = rent_price2 + rent_price1;
//          $('#qty-price').text(rent_price2);
//          price++;
//      }while(price<qty);
//    }
//    else if(qty==10){
//      temp_rent = temp_rent * 2;
//      $('#qty-price').text(temp_rent);
//    }
//    else if(qty==14){
//      do{
//          rent_price2 = rent_price2 + rent_price1;
//          $('#qty-price').text(rent_price2);
//          price++;
//      }while(price<qty);
//    }
//    else if(qty==15){
//      temp_rent = temp_rent * 3;
//      $('#qty-price').text(temp_rent);
//    }else{
//      do{
//          temp_qty_rent = temp_qty_rent - rent_price1;
//          $('#qty-price').text(temp_qty_rent);
//          price--;
//      }while(price>=qty);
//    }
//
//    }

//-------------------------------------

//for unlimited rent
//    function total3(){
//    var rent_price3=$('#rent-price3').text();
//    var qty = $('input#qty-input').val();
//    rent_price3 = rent_price3 * qty;
//    $('#qty-price').text(rent_price3);
//    }
//    function total_minus3(){
//    var rent_price3=$('#rent-price3').text();
//    var qty = $('input#qty-input').val();
//    rent_price3 = rent_price3 / qty;
//    $('#qty-price').text(rent_price3);
//    }
//-------------------------------

//------------------------------


//days amount addition---------------------------




//===========================================



//--------add to cart operation------------
var cart_count = $('.badge').text();
    if(cart_count >= 1){
        $('.badge').css({"display": "inline-block"});
    }else{
        $('.badge').css({"display": "none"});
    }


//---------------------------------------

//-----------login_popup_close-------------

$('#popup_close').click(function(){
    $('.login_popup_banner').fadeOut();
    $('.login-popup').css({"opacity": "0", "transform": "scale(.05)"});
});

//=====================================

//------rating_properties-----------------


//=============================================

//----rate-progress bar--------------
var total = parseInt($('#total').val());
var rate_count1 = parseInt($('#rate_count1').text());
var rate_count2 = parseInt($('#rate_count2').text());
var rate_count3 = parseInt($('#rate_count3').text());
var rate_count4 = parseInt($('#rate_count4').text());
var rate_count5 = parseInt($('#rate_count5').text());

var RateBarWidth1 = rate_count1 / total * 100;
$('.bar1').css({ width: RateBarWidth1 + "%" });

var RateBarWidth2 = rate_count2 / total * 100;
$('.bar2').css({ width: RateBarWidth2 + "%" });

var RateBarWidth3 = rate_count3 / total * 100;
$('.bar3').css({ width: RateBarWidth3 + "%" });

var RateBarWidth4 = rate_count4 / total * 100;
$('.bar4').css({ width: RateBarWidth4 + "%" });

var RateBarWidth5 = rate_count5 / total * 100;
$('.bar5').css({ width: RateBarWidth5 + "%" });


//=================================

//----------average star-------------

var avg_rate = $('#rate1').text();
if(avg_rate == 'None'){
    $('#rate1').text(0);
}
if(avg_rate == 1.0){
    $('#rate1').text(1);
    $('#rate_stars i:nth-child(1)').css({"color": "#FFD700"});
    $('#star_avg2').css({"display": "inline"});
    $('#star_avg1half').css({"display": "none"});
}
if(avg_rate == 2.0){
    $('#rate1').text(2);
    $('#rate_stars i:nth-child(-n+3)').css({"color": "#FFD700"});
    $('#star_avg3').css({"display": "inline"});
    $('#star_avg2half').css({"display": "none"});
}
if(avg_rate == 3.0){
    $('#rate1').text(3);
    $('#rate_stars i:nth-child(-n+5)').css({"color": "#FFD700"});
    $('#star_avg4').css({"display": "inline"});
    $('#star_avg3half').css({"display": "none"});
}
if(avg_rate == 4.0){
    $('#rate1').text(4);
    $('#rate_stars i:nth-child(-n+7)').css({"color": "#FFD700"});
    $('#star_avg5').css({"display": "inline"});
    $('#star_avg4half').css({"display": "none"});
}
if(avg_rate == 5.0){
    $('#rate1').text(5);
    $('#rate_stars i:nth-child(n)').css({"color": "#FFD700"});
    $('#star_avg5').css({"display": "inline"});
    $('#star_avg4half').css({"display": "none"});
}
if(avg_rate > 1 && avg_rate < 2){
    $('#rate_stars i:nth-child(-n+2)').css({"color": "#FFD700"});
    $('#star_avg2').css({"display": "none"});
    $('#star_avg1half').css({"display": "inline"});
}
if(avg_rate > 2 && avg_rate < 3){
    $('#rate_stars i:nth-child(-n+5)').css({"color": "#FFD700"});
    $('#star_avg3').css({"display": "none"});
    $('#star_avg2half').css({"display": "inline"});
}
if(avg_rate > 3 && avg_rate < 4){
    $('#rate_stars i:nth-child(-n+6)').css({"color": "#FFD700"});
    $('#star_avg4').css({"display": "none"});
    $('#star_avg3half').css({"display": "inline"});
}
if(avg_rate > 4 && avg_rate < 5){
    $('#rate_stars i:nth-child(n)').css({"color": "#FFD700"});
    $('#star_avg5').css({"display": "none"});
    $('#star_avg4half').css({"display": "inline"});
}

//======================================


//--------query-display-method-------------------

$('.answer_area:has(.answer:empty)').remove();

$('#question_log_pop').click(function(){
    $('#error-info').empty();
    $('.login_popup_banner').fadeIn();
    $('.login-popup').css({"opacity": "1", "transform": "scale(1)"});
});

//===========================================

