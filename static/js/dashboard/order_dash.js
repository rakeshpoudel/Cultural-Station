$('.view_detail').on('click', function(){
	var idstr = this.id.toString();
	$('.history_content').hide();
	$('#o'+idstr).show();
	$('.detail_popup_banner').fadeIn();
	$('.details_pop').css({"transform": "scale(1)", "opacity": "1"});
});
$('.order_list').on('click', function(){
	var ids = $(this).attr("data");
	var idstr = ids.toString();
	$('.history_content').hide();
	$('#o'+idstr).show();
	$('.detail_popup_banner').fadeIn();
	$('.details_pop').css({"transform": "scale(1)", "opacity": "1"});
});
$('.results').on('click', function(){
	var idstr = this.id.toString();
	$('.history_content').hide();
	$('#o'+idstr).show();
	$('.detail_popup_banner').fadeIn();
	$('.details_pop').css({"transform": "scale(1)", "opacity": "1"});
});
$('.invoice_btn').on('click', function(){
	var idstr = this.id.toString();
	$('#invoice'+idstr).css({"transform": "scale(1)", "opacity": "1"});
});
$('.close1').click(function(){
	$('.history_content').hide();
	$('.detail_popup_banner').fadeOut();
	$('.details_pop').css({"transform": "scale(.2)", "opacity": "0"});
	$('.change_stat_contain').hide();
	$('.stat_dis').show();
	$('.stat_dis2').hide();
	$('.action_text3').show();
	$('.action_text2').show();
	$('.actions').hide();
	$('.o_error').empty();
});
$('.close2').click(function(){
	$('.invoice_banner').css({"transform": "scale(.1)", "opacity": "0"});
});
$('.change_stat').on('click', function(){
	var idstr = this.id.toString();
	$('#st'+idstr).hide();
	$('#sac'+idstr).show();

});
$('.stat_update').on('click', function(){
	var idstr = this.id.toString();
	$('#up'+idstr).hide();
	$('#ac'+idstr).hide();
	$('#act'+idstr).show();
	$('#er'+idstr).empty();

});

$('.process_refresh').on('click', function(){
	$('.order_history_content').load("/dashboard/processing-order/");
  $('.refresh_cover').load("/dashboard/order-detail/");
});
$('.recent_o_refresh').on('click', function(){
	$('.order_subbanner2').load("/dashboard/recent-order/");
});
$('.cancel_refresh').on('click', function(){
	$('.order_subbanner3').load("/dashboard/cancel-refresh/");
});
$('.returns_refresh').on('click', function(){
	$('.order_subbanner4').load("/dashboard/recent-return/");
});
$('.history_refresh').on('click', function(){
	$('.order_subbanner5').load("/dashboard/history-refresh/");
});

// $('#process_filter').mouseenter(function(){
// 	$(this).css({"background": "#01628c"});
// });
// $('#process_filter').mouseleave(function(){
// 	$(this).css({"background": "#008ECC"});
// });
// $('#complete_filter').mouseenter(function(){
// 	$(this).css({"background": "#01628c"});
// });
// $('#complete_filter').mouseleave(function(){
// 	$(this).css({"background": "#008ECC"});
// });
$('#process_filter').click(function(){
	$(this).css({"background": "#01628c"});
	$('#complete_filter').css({"background": "#008ECC"});
	$('#complete_banner').hide();
	$('#process_banner').show();
	$('#order_search_com').val('');
	$('.result_order2').hide();
});
$('#complete_filter').click(function(){
	$(this).css({"background": "#01628c"});
	$('#process_filter').css({"background": "#008ECC"});
	$('#process_banner').hide();
	$('#complete_banner').show();
	$('#order_search').val('');
	$('.result_order').hide();
});

$('.cng_btn').on('click', function(event) {
	var idstr = this.id.toString();
    $('#sp'+idstr).show();
    var o_num = $('#link_o_number'+idstr).val();
    var p_id = $('#link_p_id'+idstr).val();
    var p_size = $('#link_p_size'+idstr).val();
    var qty = $('#link_p_qty'+idstr).val();
    var formData = {
          'status': $('input[name=status]').val(),
          'qty': qty,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
      $.ajax({
              type: 'POST',
              url: '/dashboard/rental-update/'+o_num+'/'+p_id+'/'+p_size+'/',
              data: formData,
              encode: true
          })
          .done(function(data) {

                $('.refresh_cover').load("/dashboard/order-detail/");
                $('.order_subbanner4').load("/dashboard/recent-return/");
                $('#sp'+idstr).hide();

          });
      event.preventDefault();

  });

$('.action_btn3').on('click', function(event) {
	var ids = $(this).attr("data");
	var idstr = ids.toString();
    $('#cret'+idstr).show();
    var st = $(this).attr("name");
    $('#acin'+idstr).val(st);
    var stat = $('#acin'+idstr).val();
    var o_num = $('#on'+idstr).val();
    var formData = {
          'status': stat,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
      $.ajax({
              type: 'POST',
              url: '/dashboard/order-update/'+o_num+'/',
              data: formData,
              encode: true
          })
          .done(function(data) {

                // mystr = `<p style="color:green; font-size:14px;">Updated</p>`
                $('.refresh_cover').load("/dashboard/order-detail/");
                $('.order_history_content').load("/dashboard/processing-order/");
				        $('.order_subbanner2').load("/dashboard/recent-order/");
                
                //$('#o'+o_num).show();
                $('#cret'+idstr).hide();
                // $('#sac'+idstr).hide();
                // $('#stt'+idstr).show();

          });
      event.preventDefault();

  });

$('.action_btn2').on('click', function(event) {
	var ids = $(this).attr("data");
	var idstr = ids.toString();
    $('#cdel'+idstr).show();
    var st = $(this).attr("name");
    $('#acin'+idstr).val(st);
    var stat = $('#acin'+idstr).val();
    var o_num = $('#on'+idstr).val();
    var formData = {
          'status': stat,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
      $.ajax({
              type: 'POST',
              url: '/dashboard/order-update/'+o_num+'/',
              data: formData,
              encode: true
          })
          .done(function(data) {

                // mystr = `<p style="color:green; font-size:14px;">Updated</p>`
                $('.refresh_cover').load("/dashboard/order-detail/");
                $('.order_history_content').load("/dashboard/processing-order/");
                //$('#o'+o_num).show();
                $('#cdel'+idstr).show();
                // $('#sac'+idstr).hide();
                // $('#stt'+idstr).show();

          });
      event.preventDefault();

  });

$('.action_btn1').on('click', function(event) {
	var ids = $(this).attr("data");
	var idstr = ids.toString();
    $('#cship'+idstr).show();
    var st = $(this).attr("name");
    $('#acin'+idstr).val(st);
    var stat = $('#acin'+idstr).val();
    var o_num = $('#on'+idstr).val();
    var formData = {
          'status': stat,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
      $.ajax({
              type: 'POST',
              url: '/dashboard/order-update/'+o_num+'/',
              data: formData,
              encode: true
          })
          .done(function(data) {

                // mystr = `<p style="color:green; font-size:14px;">Updated</p>`
                $('.refresh_cover').load("/dashboard/order-detail/");
                $('.order_history_content').load("/dashboard/processing-order/");
                //$('#o'+o_num).show();
                $('#cship'+idstr).show();
                // $('#sac'+idstr).hide();
                // $('#stt'+idstr).show();

          });
      event.preventDefault();

  });

$('.view_new_detail').on('click', function(event) {
	var idstr = this.id.toString();
    var check = $('#check'+idstr).val();
    var o_num = $('#con'+idstr).val();
    var formData = {
          'check': check,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
      $.ajax({
              type: 'POST',
              url: '/dashboard/check-status/'+o_num+'/',
              data: formData,
              encode: true
          })
          .done(function(data) {

				$('.history_content').hide();
				$('#o'+idstr).show();
				$('.detail_popup_banner').fadeIn();
				$('.details_pop').css({"transform": "scale(1)", "opacity": "1"});
				// $('.order_history_content').load("/dashboard/processing-order/");
        $('#notification_dropdown').load("/dashboard/o-notification/");

          });
      event.preventDefault();

  });