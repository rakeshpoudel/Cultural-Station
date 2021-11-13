//--logout/log_in_page function--------------------------

function logout(){
    var form = document.forms['logout_form'];
    form.submit();
}
//============================
var cart_counted = parseInt($('.badge').text());
if(cart_counted >= 1){
    $('.badge').css({"display": "inline-block"});
}else{
    $('.badge').css({"display": "none"});
}
//======================

//========header-function----------------

var height = $('.header').height();
// $('.row:first-child').css({"margin-top": height-5 + "px"});
$(window).scroll(function(){
    var scroll = $(window).scrollTop();

    if (scroll > height) {
        $('.hidden_header').slideDown(100);
        $('.menu-dropdown-banner').hide();
    }else{
       $('.hidden_header').slideUp(100);
       $('.hidden-menu-dropdown-banner').slideUp(100);
    }
});
// $(window).scroll(function(){
//     var maxHeight;
//     var top_m;
//     var top_t;
//     var scroll = $(window).scrollTop();

//     if (scroll > height) {
//         maxHeight = 70;
//         top_m = 15;
//         top_t = 5;
//     }else{
//        maxHeight = 100;
//        top_m = 30;
//        top_t = 20;
//     }
//     $('.sub-header').stop().animate({"line-height": maxHeight + "px"}, 200);
//     $('.sub-header1').stop().animate({"height": maxHeight + "px"}, 200);
//     $('.cart_badge').stop().animate({"line-height": maxHeight + "px"}, 200);
//     $('#search-icon').stop().animate({"line-height": maxHeight + "px"}, 200);
//     $('#user-dropdown').stop().animate({"line-height": maxHeight + "px"}, 200);
//     $('#signin-dropdown').stop().animate({"line-height": maxHeight + "px"}, 200);
//     $('.menus ul').stop().animate({"line-height": maxHeight + "px"}, 200);
//     $('.menus ul a').stop().animate({"padding": "35px 0px"}, 200);
//     $('.line').stop().animate({"margin-top": top_m + "px"}, 200);
//     $('.badge').stop().animate({"top": top_t + "px"}, 200);
//     $('.menu-dropdown-banner').css({"top": maxHeight + "px"});
// //    $('.menu-dropdown-banner').css({"position":"fixed", "left": "0px", "z-index": "99"});
// });

//======================================
//sticky.removeClass('fixed');
//    $('.sub-header').css({"line-height": "100px"});
//    $('.sub-header1').css({"height": "100px"});
//    $('.cart_badge').css({"line-height": "100px"});
//    $('#search-icon').css({"line-height": "100px"});
//    $('#user-dropdown').css({"line-height": "100px"});
//    $('#signin-dropdown').css({"line-height": "100px"});
//    $('.menus ul').css({"line-height": "100px"});
//    $('.menus ul a').css({"padding": "50px 0px"});
//    $('.line').css({"margin-top": "30px"});
//    $('.badge').css({"top": "20px"});
//    $('.menu-dropdown-banner').css({"position":"absolute", "left": "0px", "z-index": "9"});
//    $('.menu-dropdown-banner').css('top', '0px');

// menu drop down---------------------------
var drop=0;
var drop1=0;
$('.drop-menu').mouseenter(function(){
    $('.menu-dropdown-banner').show();
});
$('.menu-dropdown-banner').mouseenter(function(){
       $('.menu-dropdown-banner').css({"display": "block"});
       $('.drop-menu').css({"color": "#fc9730"});
       $('.chevron-menu').css({"color": "#fc9730"});
 });
$('.drop-menu').mouseleave(function(){
    $('.menu-dropdown-banner').hide();
});
$('.menu-dropdown-banner').mouseleave(function(){
       $('.menu-dropdown-banner').hide();
       $('.drop-menu').css({"color": "#fff !important"});
       $('.chevron-menu').css({"color": "#d69f67"});
 });

$('.drop-menu1').mouseenter(function(){
    $('.hidden-menu-dropdown-banner').show();
});
$('.hidden-menu-dropdown-banner').mouseenter(function(){
       $('.hidden-menu-dropdown-banner').css({"display": "block"});
       $('.drop-menu1').css({"color": "#fc9730"});
       $('.chevron-menu').css({"color": "#fc9730"});
 });
$('.drop-menu1').mouseleave(function(){
    $('.hidden-menu-dropdown-banner').hide();
});
$('.hidden-menu-dropdown-banner').mouseleave(function(){
       $('.hidden-menu-dropdown-banner').hide();
       $('.drop-menu1').css({"color": "#fff !important"});
       $('.chevron-menu').css({"color": "#d69f67"});
 });
//=========================================


// animations------------------------------------

setTimeout(function(){
  $('.main-text1').css({"transform" : "translateY(0px)", "opacity" : "1"});
});
setTimeout(function(){
  $('.main-button').css({"transform" : "translateY(0px)", "opacity" : "1"});
}, 500);

setTimeout(function(){
    $('#slidetext1').css({"transform" : "translateX(0px)", "opacity": "1"});
    $('#slidetext1').css({"-moz-transform" : "translateX(0px)", "opacity": "1"});
});
setTimeout(function(){
    $('#slidetext2').css({"transform" : "translateX(0px)", "opacity": "1"});
    $('#slidetext2').css({"-moz-transform" : "translateX(0px)", "opacity": "1"});
}, 500);
setTimeout(function(){
    $('#slidetext3').css({"transform" : "translateX(0px)", "opacity": "1"});
    $('#slidetext3').css({"-moz-transform" : "translateX(0px)", "opacity": "1"});
}, 1000);

//--------------------------------------------------------

//rating & review

setTimeout(function(){
  $('.rating_popup_banner').fadeIn();
  $('.rating_pop').css({"transform" : "translateY(50px)", "opacity" : "1"});
}, 800);

//======================

// ratings=====================================

$('#rate_btn').prop("disabled", true);
$('.rating i').click(function(){
    $('#rate_btn').prop("disabled", false);
});
$('.rating #star5').click(function(){
    $('.rating #star_check5').prop('checked', true);

});
$('.rating #star4').click(function(){
    $('.rating #star_check4').prop('checked', true);
});
$('.rating #star3').click(function(){
    $('.rating #star_check3').prop('checked', true);
});
$('.rating #star2').click(function(){
    $('.rating #star_check2').prop('checked', true);
});
$('.rating #star1').click(function(){
    $('.rating #star_check1').prop('checked', true);
});

//=================================================

$('#popup_close_review_rate').click(function(){
  $('.rating_popup_banner').fadeOut();
  $('.rating_pop').css({"transform" : "translateY(0px)", "opacity" : "0"});
});


// chatbot functionality-----------------

setTimeout(function(){
  $('.chat_info').fadeIn();
  $('.chat_info').css({"transform" : "translateX(0px)"});
}, 2000);
setTimeout(function(){
  $('.chat_info').fadeOut();
  $('.chat_info').css({"transform" : "translateX(-20px)"});
}, 6000);

$('.chaton').click(function(){
  $('.chat').hide();
  $('.main_chatbot').slideDown(200);
  $('#chat_input').focus();
});
$('#dottext').click(function(){
  $('.chat').hide();
  $('.main_chatbot').slideDown(200);
  $('#chat_input').focus();
});
$('#chat_icon2').on('click', function(){
  $('.main_chatbot').slideUp(200);
  $('.chat').show();
});

$('.event_main_banner').fadeIn();
$('.d_event_content').css({"margin-top": "120px", "opacity": "1"});
$('#event_close').click(function(){
  $('.event_main_banner').fadeOut();
  $('.d_event_content').css({"margin-top": "0px", "opacity": "0"});
});

// function addContent(){
//   var msgdiv = document.getElementById('scroll_data');
//   scrollAtBottom(msgdiv);
// }

//===============================

// cart functionality-----------------

//  $('#popcart').popover();
//  // Find out the cart items from localStorage
//  if (localStorage.getItem('cart') == null) {
//    var cart = {};
//  } else {
//    cart = JSON.parse(localStorage.getItem('cart'));
//    // document.getElementById('cart').innerHTML = Object.keys(cart).length;
//    updateCart(cart);
//
//  }
//  // If the add to cart button is clicked, add/increment the item
//  // $('.cart').click(function() {
//  $('.divpr').on('click', 'button.cart', function(){
//    var idstr = this.id.toString();
//    if (cart[idstr] != undefined) {
//      qty = cart[idstr][0] + 1;
//    } else {
//      qty = 1;
//      name = document.getElementById('name'+idstr).innerHTML;
//      price = document.getElementById('price'+idstr).innerHTML;
//      cart[idstr] = [qty, name, parseInt(price)];
//    }
//    updateCart(cart);
//
//  });
//  //Add Popover to cart
//  updatePopover(cart);
//  function updatePopover(cart)
//  {
//    var popStr = "";
//    popStr = popStr + "<h5> Cart for your items in my shopping cart </h5><div class='mx-2 my-2'>";
//    var i = 1;
//    for (var item in cart){
//      popStr = popStr + "<b>" + i + "</b>. ";
//      popStr = popStr + document.getElementById('name' + item).innerHTML.slice(0, 19) + "... Qty: " + cart[item][0] + '<br>';
//      i = i+1;
//    }
//    popStr = popStr + "</div> <a href='/checkout'><button class='btn btn-primary' id ='checkout'>Checkout</button></a> <button class='btn btn-primary' onclick='clearCart()' id ='clearCart'>Clear Cart</button>"
//    document.getElementById('popcart').setAttribute('data-content', popStr);
//  }
//  function clearCart() {
//    cart = JSON.parse(localStorage.getItem('cart'));
//    for (var item in cart) {
//      document.getElementById('div' + item).innerHTML = '<button id="' + item + '" class="btn btn-primary cart">Add To Cart</button>'
//    }
//    localStorage.clear();
//    cart = {};
//    updatePopover(cart);
//    updateCart(cart);
//  }
//  function updateCart(cart) {
//    var sum = 0;
//    for (var item in cart) {
//      sum = sum + cart[item][0];
//      document.getElementById('div' + item).innerHTML = '<button id="minus' + item + '" class="btn btn-primary minus">-</button> <span id="val' + item + '"">' + cart[item][0] + '</span> <button id="plus' + item + '" class="btn btn-primary plus"> + </button>';
//    }
//    localStorage.setItem('cart', JSON.stringify(cart));
//    console.log(cart);
//    document.getElementById('cart').innerHTML = sum;
//    updatePopover(cart);
//  }
//  // If plus or minus button is clicked, change the cart as well as the display value
//  $('.divpr').on("click", "button.minus", function() {
//    a = this.id.slice(7, );
//    cart['pr' + a][0] = cart['pr' + a][0] - 1;
//    cart['pr' + a][0] = Math.max(0, cart['pr' + a][0]);
//    document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
//    updateCart(cart);
//  });
//  $('.divpr').on("click", "button.plus", function() {
//    a = this.id.slice(6, );
//    cart['pr' + a][0] = cart['pr' + a][0] + 1;
//    document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
//    updateCart(cart);
//  });
//
//

  //---------------------------------------------------
