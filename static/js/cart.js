window.addEventListener( "pageshow", function ( event ) {
  var historyTraversal = event.persisted ||
                         ( typeof window.performance != "undefined" &&
                              window.performance.navigation.type === 2 );
  if ( historyTraversal ) {
    // Handle page restore.
    window.location.reload();
  }
});


$('#proceed_checkout_btn').prop("disabled", true);
$('.prod_check').on('click', function(){
    var idstr = this.id.toString();
    var checked_prod=[];
    var unchecked_prod=[];
    var prod_quantity = [];
    var prod_unquantity = [];
    var prod_dates = [];
    var prod_nondates = [];
    var sum_qty = 0;
    var same;
    var error = 0;

var c_len = $('.prod_check:checked').length;
    console.log(c_len);

    $('.prod_check').each(function(){
        var $this = $(this);

        if($(this).prop("checked") == true){
        $('#proceed_checkout_btn').prop("disabled", false);
//            checked_prod.push($this.attr("value"));
            prod_quantity.push($this.attr("size"));
            prod_dates.push($this.attr("name"));
            $('.text_sub2').css({"display": "inline"});


        }else{
//            unchecked_prod.push($this.attr("value"));
            prod_unquantity.push($this.attr("size"));
            prod_nondates.push($this.attr("name"));
            $('.text_sub2').css({"display": "none"});

        }
    });

    $.each(prod_quantity,function(){sum_qty+=parseInt(this) || 0;});
//    same = AllTheSame(checked_prod);
    sameDate = AllTheSameDate(prod_dates);
//    console.log(prod_dates);
//     console.log(prod_nondates);
//    console.log(sum_qty);
//    console.log(checked_prod);
//    console.log(unchecked_prod);
//    console.log(same);

    if(sameDate == false){
        $('.amount_block').css({"display": "none"});
        $(".text_sub2, #noterror").css({"display": "none"});
        $("#error, .text_sub1, .cart_error2").css({"display": "inline"});
        $('#proceed_checkout_btn').prop("disabled", true);
        error = 1;
    }else{
        $(".text_sub2, #noterror").css({"display": "inline"});
        $('.amount_block').css({"display": "block"});
        $("#error, .text_sub1, .cart_error2").css({"display": "none"});
        $('#proceed_checkout_btn').prop("disabled", false);
        error = 0;
    }


    if($(this).prop("checked") == true){
        $('.text_sub').css({"display": "none"});

        var refund = document.getElementById('refund'+idstr).value;
        var refund_amount = parseInt($('input[name=refund_amount]').val());

        var prod_item_count = parseInt($('#summary_items').val());
        var prod_items = document.getElementById('items'+idstr).innerHTML;

        var sub_total = parseInt($('input[name=sub_total_amount]').val());
        var item_amount = document.getElementById('price'+idstr).innerHTML;

        var total_amount = parseInt($('input[name=total_amount]').val());

        prod_items = parseInt(prod_items);
        prod_item_count = prod_item_count + prod_items;
        $('#summary_items').val(prod_item_count);

        item_amount = parseInt(item_amount);
        sub_total = sub_total + item_amount;
        $('input[name=sub_total_amount]').val(sub_total);

        refund = parseInt(refund);
        refund_amount = refund_amount + refund;
        $('input[name=refund_amount]').val(refund_amount);

        total_amount = sub_total + refund_amount;
        $('input[name=total_amount]').val(total_amount);

       $("#hidden_inputs").append('<input type="text" name="prod_ids" id="inpr'+idstr+'" value='+idstr+'>');

        if($('input[name=sub_total_amount]').val() != 0){
            $('.total3').css({"display": "block"});
        }else{
            $('.total3').css({"display": "none"});
        }


    }else{
    if(c_len == 0){
        $('#proceed_checkout_btn').prop("disabled", true);
    }
    $('.text_sub').css({"display": "none"});
        var refund = document.getElementById('refund'+idstr).value;
        var refund_amount = parseInt($('input[name=refund_amount]').val());
        var prod_item_count = parseInt($('#summary_items').val());
        var prod_items = document.getElementById('items'+idstr).innerHTML;
        var sub_total = parseInt($('input[name=sub_total_amount]').val());
        var item_amount = document.getElementById('price'+idstr).innerHTML;
        var total_amount = parseInt($('input[name=total_amount]').val());

        prod_items = parseInt(prod_items);
        prod_item_count = prod_item_count - prod_items;
        $('#summary_items').val(prod_item_count);

        item_amount = parseInt(item_amount);
        sub_total = sub_total - item_amount;
        $('input[name=sub_total_amount]').val(sub_total);

        refund = parseInt(refund);
        refund_amount = refund_amount - refund;
        $('input[name=refund_amount]').val(refund_amount);

        total_amount = sub_total + refund_amount;
        $('input[name=total_amount]').val(total_amount);

        $('#inpr'+idstr+'').remove();

        if($('input[name=sub_total_amount]').val() != 0){
            $('.total3').css({"display": "block"});
        }else{
            $('.total3').css({"display": "none"});
        }

    }

    var items_counter = $('#summary_items').val();
    $('.item_error').css({"display": "none"});
    $('span#recent_item').empty();
    $('span#rent_counter').empty();
    $('span#recent_rent_way').empty();
    if(error == 0){
        if(checked_prod[0] == 'One time rental'){
            if(items_counter > 4){
                $('span#recent_item').text(items_counter);
                $('span#rent_counter').text('4');
                $('span#recent_rent_way').text(checked_prod[0]);
                $('.item_error').css({"display": "block"});
                $('.amount_block').css({"display": "none"});
                $('.cart_error2').css({"display": "block"});
                $('#proceed_checkout_btn').prop("disabled", true);
            }else{
                $('.item_error').css({"display": "none"});
                $('.cart_error2').css({"display": "none"});
                $('.amount_block').css({"display": "block"});
                $('#proceed_checkout_btn').prop("disabled", false);
            }
        }
//        if(checked_prod[0] == 'Unlimited Rent'){
//            if(items_counter > 4){
//                $('span#recent_item').text(items_counter);
//                $('span#rent_counter').text('4');
//                $('span#recent_rent_way').text(checked_prod[0]);
//                $('.item_error').css({"display": "block"});
//                $('.amount_block').css({"display": "none"});
//                $('.cart_error2').css({"display": "block"});
//                $('#proceed_checkout_btn').prop("disabled", true);
//            }else{
//                $('.item_error').css({"display": "none"});
//                $('.cart_error2').css({"display": "none"});
//                $('.amount_block').css({"display": "block"});
//                $('#proceed_checkout_btn').prop("disabled", false);
//            }
//        }
//        if(checked_prod[0] == 'Event Rent'){
//            if(items_counter > 15){
//                $('span#recent_item').text(items_counter);
//                $('span#rent_counter').text('15');
//                $('span#recent_rent_way').text(checked_prod[0]);
//                $('.item_error').css({"display": "block"});
//                $('.amount_block').css({"display": "none"});
//                $('.cart_error2').css({"display": "block"});
//                $('#proceed_checkout_btn').prop("disabled", true);
//            }else{
//                $('.item_error').css({"display": "none"});
//                $('.cart_error2').css({"display": "none"});
//                $('.amount_block').css({"display": "block"});
//                $('#proceed_checkout_btn').prop("disabled", false);
//            }
//        }
    }



});

//function AllTheSame(checked_prod) {
//    var first = checked_prod[0];
//    return checked_prod.every(function(element) {
//        return element === first;
//    });
//}
function AllTheSameDate(prod_dates) {
    var first = prod_dates[0];
    return prod_dates.every(function(element) {
        return element === first;
    });
}

$('.wish_btn_add').on('click', function(event) {
    var idp = this.id;
    var pid = $(this).attr('name');
    $('#spin'+idp).show();
    var product_name = document.getElementById('namep'+idp).value;
    var element_type = document.getElementById('elementp'+idp).value;
    var caste_type = document.getElementById('castep'+idp).value;
    var product_size = document.getElementById('sizep'+idp).value;
    var image = document.getElementById('imgp'+idp).value;


        var formData = {
        'product_name': product_name,
        'element_type': element_type,
        'caste_type': caste_type,
        'product_size': product_size,
        'image': image,
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
    };
    $.ajax({
            type: 'POST',
            url: '/shop/add_to_wishlist/'+pid+'/',
            data: formData,
            encode: true
        })
        .done(function(data) {
            $('#form'+idp).css({"display":"none"});
            $('#wish'+idp).css({"display":"inline"});
            $('#spin'+idp).hide();

        });

    event.preventDefault();
});

$('.d_cart').on('click', function(){
    var idp = this.id;
    $('#spin'+idp).show();
});
