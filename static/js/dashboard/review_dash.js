$('.select_btn').click(function(){
	$('.product_contain').show();
});
$('.close_contain').click(function(){
	$('.product_contain').hide();
});

$('.p_content').on('click', function(){
	var idstr = this.id.toString();
	$('.show_cover').hide();
	$('.re'+idstr).show();
	var text = $('.re'+idstr).text();
	$('.review_popup_banner').fadeIn();
	$('.content_pop').css({"transform": "scale(1)", "opacity": "1"});
	if(text==''){
		$('.empty').show();
	}
});
$('.q_content').on('click', function(){
	var idstr = this.id.toString();
	$('.show_cover').hide();
	$('.qu'+idstr).show();
	var text = $('.qu'+idstr).text();
	$('.review_popup_banner').fadeIn();
	$('.content_pop').css({"transform": "scale(1)", "opacity": "1"});
	if(text==''){
		$('.empty').show();
	}
});

$('.pop_close').click(function(){
	$('.show_cover').hide();
	$('.empty').hide();
	$('.review_popup_banner').fadeOut();
	$('.content_pop').css({"transform": "scale(.2)", "opacity": "0"});
});

$('.contain_refresh1').on('click', function(){
	$('.xsubcontainer2').load("/dashboard/recent-review-dash/");
});
$('.contain_refresh2').on('click', function(){
	$('.xsubcontainer3').load("/dashboard/review-dash/");
});
$('.contain_refresh4').on('click', function(){
	$('.xsub2').load("/dashboard/recent-query-dash/");
});
$('.contain_refresh5').on('click', function(){
	$('.xsub3').load("/dashboard/query-dash/");
});
// $('.contain_refresh6').on('click', function(){
// 	$('.xsub2').load("/dashboard/query-filter/");
// });
// $('.contain_refresh3').on('click', function(){
// 	$('.xsub3').load("/dashboard/review-filter/");
// });



$('.ans_btn').on('click', function(event) {
	var idstr = this.id.toString();
    $('#asp'+idstr).show();
    var answer = $('#ain'+idstr).val();
    var formData = {
          'answer': answer,
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      }
      $.ajax({
              type: 'POST',
              url: '/dashboard/answer-update/'+idstr+'/',
              data: formData,
              encode: true
          })
          .done(function(data) {

                $('.xsub2').load("/dashboard/recent-query-dash/");
                $('.query_detail').load("/dashboard/query-filter/");
                $('.xsub3').load("/dashboard/query-dash/");
                $('#asp'+idstr).hide();

          });
      event.preventDefault();

  });

//----------average star-------------

// var avg_rate = $('#rate1').val();
// if(avg_rate == 'None'){
//     $('#rate1').text(0);
// }
// if(avg_rate == 1.0){
//     $('#rate_stars i:nth-child(1)').css({"color": "#FFD700"});
//     $('#star_avg2').css({"display": "inline"});
//     $('#star_avg1half').css({"display": "none"});
// }
// if(avg_rate == 2.0){
//     $('#rate_stars i:nth-child(-n+3)').css({"color": "#FFD700"});
//     $('#star_avg3').css({"display": "inline"});
//     $('#star_avg2half').css({"display": "none"});
// }
// if(avg_rate == 3.0){
//     $('#rate_stars i:nth-child(-n+5)').css({"color": "#FFD700"});
//     $('#star_avg4').css({"display": "inline"});
//     $('#star_avg3half').css({"display": "none"});
// }
// if(avg_rate == 4.0){
//     $('#rate_stars i:nth-child(-n+7)').css({"color": "#FFD700"});
//     $('#star_avg5').css({"display": "inline"});
//     $('#star_avg4half').css({"display": "none"});
// }
// if(avg_rate == 5.0){
//     $('#rate_stars i:nth-child(n)').css({"color": "#FFD700"});
//     $('#star_avg5').css({"display": "inline"});
//     $('#star_avg4half').css({"display": "none"});
// }
// if(avg_rate > 1 && avg_rate < 2){
//     $('#rate_stars i:nth-child(-n+2)').css({"color": "#FFD700"});
//     $('#star_avg2').css({"display": "none"});
//     $('#star_avg1half').css({"display": "inline"});
// }
// if(avg_rate > 2 && avg_rate < 3){
//     $('#rate_stars i:nth-child(-n+5)').css({"color": "#FFD700"});
//     $('#star_avg3').css({"display": "none"});
//     $('#star_avg2half').css({"display": "inline"});
// }
// if(avg_rate > 3 && avg_rate < 4){
//     $('#rate_stars i:nth-child(-n+6)').css({"color": "#FFD700"});
//     $('#star_avg4').css({"display": "none"});
//     $('#star_avg3half').css({"display": "inline"});
// }
// if(avg_rate > 4 && avg_rate < 5){
//     $('#rate_stars i:nth-child(n)').css({"color": "#FFD700"});
//     $('#star_avg5').css({"display": "none"});
//     $('#star_avg4half').css({"display": "inline"});
//}

//======================================