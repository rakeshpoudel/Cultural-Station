$('#cash_btn1').addClass('select_cash');
$('.cash1').addClass('cash3');
$('#pay_contain1').show();

$('#order_confirm_btn').on('click', function(){
    $('.spinner4').show();
});
$('#esewa_pay_btn').on('click', function(){
    $('.spinner6').show();
});
$('khalti_pay_btn3').on('click', function(){
    $('.spinner5').show();
});

$('#cash_btn1').click(function(){
    $('#cash_btn2').removeClass('select_cash');
    $('#cash_btn3').removeClass('select_cash');
    $('#cash_btn4').removeClass('select_cash');
    $('.cash2').removeClass('cash4');
    $('.cash3').removeClass('cash4');
    $('.cash5').removeClass('cash4');
    $('#pay_contain2').hide();
    $('#pay_contain3').hide();
    $('#cash_btn1').addClass('select_cash');
    $('.cash1').addClass('cash4');
    $('#pay_contain1').show();
    $('#pay_contain2').hide();
    $('#pay_contain3').hide();
    $('#pay_contain4').hide();
    $('#pay_contain5').hide();
    $('#pay_contain6').hide();
});
$('#cash_btn2').click(function(){
    $('#cash_btn2').addClass('select_cash');
    $('#cash_btn3').removeClass('select_cash');
    $('.cash2').addClass('cash4');
    $('#pay_contain2').show();
    $('#cash_btn1').removeClass('select_cash');
    $('.cash1').removeClass('cash4');
    $('.cash3').removeClass('cash4');
    $('.cash5').removeClass('cash4');
    $('#cash_btn4').removeClass('select_cash');
    $('#pay_contain1').hide();
    $('#pay_contain3').hide();
    $('#pay_contain4').hide();
    $('#pay_contain5').hide();
});
$('#cash_btn3').click(function(){
    $('#cash_btn3').addClass('select_cash');
    $('.cash3').addClass('cash4');
    $('.cash2').removeClass('cash4');
    $('.cash1').removeClass('cash4');
    $('.cash5').removeClass('cash4');
    $('#pay_contain2').show();
    $('#cash_btn1').removeClass('select_cash');
    $('#cash_btn2').removeClass('select_cash');
    $('#cash_btn4').removeClass('select_cash');
    $('#pay_contain1').hide();
    $('#pay_contain2').hide();
    $('#pay_contain4').hide();
    $('#pay_contain3').show();
    $('#pay_contain5').hide();
    $('#pay_contain6').hide();
});
$('#cash_btn4').click(function(){
    $('#cash_btn4').addClass('select_cash');
    $('.cash5').addClass('cash4');
    $('.cash2').removeClass('cash4');
    $('.cash1').removeClass('cash4');
    $('.cash3').removeClass('cash4');
    $('#pay_contain6').show();
    $('#cash_btn1').removeClass('select_cash');
    $('#cash_btn2').removeClass('select_cash');
    $('#cash_btn3').removeClass('select_cash');
    $('#pay_contain1').hide();
    $('#pay_contain2').hide();
    $('#pay_contain4').hide();
    $('#pay_contain3').hide();
    $('#pay_contain5').hide();
});


$('#khalti_pay_btn').click(function(){
   mobile = $('input[name=mobile_number]').val(); 
   $('#mobile_khalti').text(mobile);
   $('#pay_contain3').hide();
   $('#pay_contain4').show();
});
$('#khalti_pay_btn2').click(function(){
   $('#pay_contain4').hide();
   $('#pay_contain5').show();
});


