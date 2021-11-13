var main_count = $('#t_count').val();
if(main_count=="None"){
	main_count = 0;
	$('#count1').text(0);
}
console.log(main_count);
round();

var man_jan = $('#man_jan').val();
if(man_jan=="None"){
	man_jan=0;
}
var woman_jan = $('#woman_jan').val();
if(woman_jan=="None"){
	woman_jan=0;
}
var man_feb = $('#man_feb').val();
if(man_feb=="None"){
	man_feb=0;
}
var woman_feb = $('#woman_feb').val();
if(woman_feb=="None"){
	woman_feb=0;
}
var man_mar = $('#man_mar').val();
if(man_mar=="None"){
	man_mar=0;
}
var woman_mar = $('#woman_mar').val();
if(woman_mar=="None"){
	woman_mar=0;
}
var man_apr = $('#man_apr').val();
if(man_apr=="None"){
	man_apr=0;
}
var woman_apr = $('#woman_apr').val();
if(woman_apr=="None"){
	woman_apr=0;
}
var man_may = $('#man_may').val();
if(man_may=="None"){
	man_may=0;
}
var woman_may = $('#woman_may').val();
if(woman_may=="None"){
	woman_may=0;
}
var man_jun = $('#man_jun').val();
if(man_jun=="None"){
	man_jun=0;
}
var woman_jun = $('#woman_jun').val();
if(woman_jun=="None"){
	woman_jun=0;
}
var man_jul = $('#man_jul').val();
if(man_jul=="None"){
	man_jul=0;
}
var woman_jul = $('#woman_jul').val();
if(woman_jul=="None"){
	woman_jul=0;
}
var man_aug = $('#man_aug').val();
if(man_aug=="None"){
	man_aug=0;
}
var woman_aug = $('#woman_aug').val();
if(woman_aug=="None"){
	woman_aug=0;
}
var man_sep = $('#man_sep').val();
if(man_sep=="None"){
	man_sep=0;
}
var woman_sep = $('#woman_sep').val();
if(woman_sep=="None"){
	woman_sep=0;
}
var man_oct = $('#man_oct').val();
if(man_oct=="None"){
	man_oct=0;
}
var woman_oct = $('#woman_oct').val();
if(woman_oct=="None"){
	woman_oct=0;
}
var man_nov = $('#man_nov').val();
if(man_nov=="None"){
	man_nov=0;
}
var woman_nov = $('#woman_nov').val();
if(woman_nov=="None"){
	woman_nov=0;
}
var man_dec = $('#man_dec').val();
if(man_dec=="None"){
	man_dec=0;
}
var woman_dec = $('#woman_dec').val();
if(woman_dec=="None"){
	woman_dec=0;
}

bar();

function round(){
	var count80 = main_count * 80/100;
	var count60 = main_count * 60/100;
	var count40 = main_count * 40/100;
	var count20 = main_count * 20/100;
	$('#count2').text(count80);
	$('#count3').text(count60);
	$('#count4').text(count40);
	$('#count5').text(count20);
	var c2 = parseInt($('#count2').text());
	var rc2 = Math.trunc(c2);
	$('#count2').text(rc2);
	var c3 = parseInt($('#count3').text());
	var rc3 = Math.trunc(c3);
	$('#count3').text(rc3);
	var c4 = parseInt($('#count4').text());
	var rc4 = Math.trunc(c4);
	$('#count4').text(rc4);
	var c5 = parseInt($('#count5').text());
	var rc5 = Math.trunc(c5);
	$('#count5').text(rc5);
}

function bar(){
	bar_man_jan = man_jan / main_count * 100;
	bar_woman_jan = woman_jan / main_count * 100;
	bar_man_feb = man_feb / main_count * 100;
	bar_woman_feb = woman_feb / main_count * 100;
	bar_man_mar = man_mar / main_count * 100;
	bar_woman_mar = woman_mar / main_count * 100;
	bar_man_apr = man_apr / main_count * 100;
	bar_woman_apr = woman_apr / main_count * 100;
	bar_man_may = man_may / main_count * 100;
	bar_woman_may = woman_may / main_count * 100;
	bar_man_jun = man_jun / main_count * 100;
	bar_woman_jun = woman_jun / main_count * 100;
	bar_man_jul = man_jul / main_count * 100;
	bar_woman_jul = woman_jul / main_count * 100;
	bar_man_aug = man_aug / main_count * 100;
	bar_woman_aug = woman_aug / main_count * 100;
	bar_man_sep = man_sep / main_count * 100;
	bar_woman_sep = woman_sep / main_count * 100;
	bar_man_oct = man_oct / main_count * 100;
	bar_woman_oct = woman_oct / main_count * 100;
	bar_man_nov = man_nov / main_count * 100;
	bar_woman_nov = woman_nov / main_count * 100;
	bar_man_dec = man_dec / main_count * 100;
	bar_woman_dec = woman_dec / main_count * 100;
	setTimeout(function(){
		if(bar_man_jan!='0'){
			$('#bar_men_jan_line').css({ height: bar_man_jan + "%" });
		}else{
			$('#bar_men_jan_line').css({ height: "1%" });
		}
	});
	setTimeout(function(){
		if(bar_woman_jan!='0'){
			$('#bar_women_jan_line').css({ height: bar_woman_jan + "%" });
		}else{
			$('#bar_women_jan_line').css({ height: "1%" });
		}
	}, 50);
	setTimeout(function(){
		if(bar_man_feb!='0'){
			$('#bar_men_feb_line').css({ height: bar_man_feb + "%" });
		}else{
			$('#bar_men_feb_line').css({ height: "1%" });
		}
	}, 100);
	setTimeout(function(){
		if(bar_woman_feb!='0'){
			$('#bar_women_feb_line').css({ height: bar_woman_feb + "%" });
		}else{
			$('#bar_women_feb_line').css({ height: "1%" });
		}
	}, 150);
	setTimeout(function(){
		if(bar_man_mar!='0'){
			$('#bar_men_mar_line').css({ height: bar_man_mar + "%" });
		}else{
			$('#bar_men_mar_line').css({ height: "1%" });
		}
	}, 200);
	setTimeout(function(){
		if(bar_woman_mar!='0'){
			$('#bar_women_mar_line').css({ height: bar_woman_mar + "%" });
		}else{
			$('#bar_women_mar_line').css({ height: "1%" });
		}
	}, 250);
	setTimeout(function(){
		if(bar_man_apr!='0'){
			$('#bar_men_apr_line').css({ height: bar_man_apr + "%" });
		}else{
			$('#bar_men_apr_line').css({ height: "1%" });
		}
	}, 300);
	setTimeout(function(){
		if(bar_woman_apr!='0'){
			$('#bar_women_apr_line').css({ height: bar_woman_apr + "%" });
		}else{
			$('#bar_women_apr_line').css({ height: "1%" });
		}
	}, 350);
	setTimeout(function(){
		if(bar_man_may!='0'){
			$('#bar_men_may_line').css({ height: bar_man_may + "%" });
		}else{
			$('#bar_men_may_line').css({ height: "1%" });
		}
	}, 400);
	setTimeout(function(){
		if(bar_woman_may!='0'){
			$('#bar_women_may_line').css({ height: bar_woman_may + "%" });
		}else{
			$('#bar_women_may_line').css({ height: "1%" });
		}
	}, 450);
	setTimeout(function(){
		if(bar_man_jun!='0'){
			$('#bar_men_jun_line').css({ height: bar_man_jun + "%" });
		}else{
			$('#bar_men_jun_line').css({ height: "1%" });
		}
	}, 500);
	setTimeout(function(){
		if(bar_woman_jun!='0'){
			$('#bar_women_jun_line').css({ height: bar_woman_jun + "%" });
		}else{
			$('#bar_women_jun_line').css({ height: "1%" });
		}
	}, 550);
	setTimeout(function(){
		if(bar_man_jul!='0'){
			$('#bar_men_jul_line').css({ height: bar_man_jul + "%" });
		}else{
			$('#bar_men_jul_line').css({ height: "1%" });
		}
	}, 600);
	setTimeout(function(){
		if(bar_woman_jul!='0'){
			$('#bar_women_jul_line').css({ height: bar_woman_jul + "%" });
		}else{
			$('#bar_women_jul_line').css({ height: "1%" });
		}
	}, 650);
	setTimeout(function(){
		if(bar_man_aug!='0'){
			$('#bar_men_aug_line').css({ height: bar_man_aug + "%" });
		}else{
			$('#bar_men_aug_line').css({ height: "1%" });
		}
	}, 700);
	setTimeout(function(){
		if(bar_woman_aug!='0'){
			$('#bar_women_aug_line').css({ height: bar_woman_aug + "%" });
		}else{
			$('#bar_women_aug_line').css({ height: "1%" });
		}
	}, 750);
	setTimeout(function(){
		if(bar_man_sep!='0'){
			$('#bar_men_sep_line').css({ height: bar_man_sep + "%" });
		}else{
			$('#bar_men_sep_line').css({ height: "1%" });
		}
	}, 800);
	setTimeout(function(){
		if(bar_woman_sep!='0'){
			$('#bar_women_sep_line').css({ height: bar_woman_sep + "%" });
		}else{
			$('#bar_women_sep_line').css({ height: "1%" });
		}
	}, 850);
	setTimeout(function(){
		if(bar_man_oct!='0'){
			$('#bar_men_oct_line').css({ height: bar_man_oct + "%" });
		}else{
			$('#bar_men_oct_line').css({ height: "1%" });
		}
	}, 900);
	setTimeout(function(){
		if(bar_woman_oct!='0'){
			$('#bar_women_oct_line').css({ height: bar_woman_oct + "%" });
		}else{
			$('#bar_women_oct_line').css({ height: "1%" });
		}
	}, 950);
	setTimeout(function(){
		if(bar_man_nov!='0'){
			$('#bar_men_nov_line').css({ height: bar_man_nov + "%" });
		}else{
			$('#bar_men_nov_line').css({ height: "1%" });
		}
	}, 1000);
	setTimeout(function(){
		if(bar_woman_nov!='0'){
			$('#bar_women_nov_line').css({ height: bar_woman_nov + "%" });
		}else{
			$('#bar_women_nov_line').css({ height: "1%" });
		}
	}, 1050);
	setTimeout(function(){
		if(bar_man_dec!='0'){
			$('#bar_men_dec_line').css({ height: bar_man_dec + "%" });
		}else{
			$('#bar_men_dec_line').css({ height: "1%" });
		}
	}, 1100);
	setTimeout(function(){
		if(bar_woman_dec!='0'){
			$('#bar_women_dec_line').css({ height: bar_woman_dec + "%" });
		}else{
			$('#bar_women_dec_line').css({ height: "1%" });
		}
	}, 1150);

}


// refresh elements==============================

$('.query_refresh').on('click', function(){
	$('#query_contain').load("/dashboard/query-refresh/");
});
$('.review_refresh').on('click', function(){
	$('#review_contain').load("/dashboard/review-refresh/");
});
$('.order_refresh').on('click', function(){
	$('#order_contain').load("/dashboard/order-refresh/");
});
$('.prent_refresh').on('click', function(){
	$('#rent_contain').load("/dashboard/rent-refresh/");
});

//================================================


$('#bar_men_jan_line').mouseenter(function(){
	$('#men_pop_jan').show();
});
$('#bar_men_jan_line').mouseleave(function(){
	$('#men_pop_jan').hide();
});
$('#bar_women_jan_line').mouseenter(function(){
	$('#women_pop_jan').show();
});
$('#bar_women_jan_line').mouseleave(function(){
	$('#women_pop_jan').hide();
});

$('#bar_men_feb_line').mouseenter(function(){
	$('#men_pop_feb').show();
});
$('#bar_men_feb_line').mouseleave(function(){
	$('#men_pop_feb').hide();
});
$('#bar_women_feb_line').mouseenter(function(){
	$('#women_pop_feb').show();
});
$('#bar_women_feb_line').mouseleave(function(){
	$('#women_pop_feb').hide();
});

$('#bar_men_mar_line').mouseenter(function(){
	$('#men_pop_mar').show();
});
$('#bar_men_mar_line').mouseleave(function(){
	$('#men_pop_mar').hide();
});
$('#bar_women_mar_line').mouseenter(function(){
	$('#women_pop_mar').show();
});
$('#bar_women_mar_line').mouseleave(function(){
	$('#women_pop_mar').hide();
});

$('#bar_men_apr_line').mouseenter(function(){
	$('#men_pop_apr').show();
});
$('#bar_men_apr_line').mouseleave(function(){
	$('#men_pop_apr').hide();
});
$('#bar_women_apr_line').mouseenter(function(){
	$('#women_pop_apr').show();
});
$('#bar_women_apr_line').mouseleave(function(){
	$('#women_pop_apr').hide();
});

$('#bar_men_may_line').mouseenter(function(){
	$('#men_pop_may').show();
});
$('#bar_men_may_line').mouseleave(function(){
	$('#men_pop_may').hide();
});
$('#bar_women_may_line').mouseenter(function(){
	$('#women_pop_may').show();
});
$('#bar_women_may_line').mouseleave(function(){
	$('#women_pop_may').hide();
});

$('#bar_men_jun_line').mouseenter(function(){
	$('#men_pop_jun').show();
});
$('#bar_men_jun_line').mouseleave(function(){
	$('#men_pop_jun').hide();
});
$('#bar_women_jun_line').mouseenter(function(){
	$('#women_pop_jun').show();
});
$('#bar_women_jun_line').mouseleave(function(){
	$('#women_pop_jun').hide();
});

$('#bar_men_jul_line').mouseenter(function(){
	$('#men_pop_jul').show();
});
$('#bar_men_jul_line').mouseleave(function(){
	$('#men_pop_jul').hide();
});
$('#bar_women_jul_line').mouseenter(function(){
	$('#women_pop_jul').show();
});
$('#bar_women_jul_line').mouseleave(function(){
	$('#women_pop_jul').hide();
});

$('#bar_men_aug_line').mouseenter(function(){
	$('#men_pop_aug').show();
});
$('#bar_men_aug_line').mouseleave(function(){
	$('#men_pop_aug').hide();
});
$('#bar_women_aug_line').mouseenter(function(){
	$('#women_pop_aug').show();
});
$('#bar_women_aug_line').mouseleave(function(){
	$('#women_pop_aug').hide();
});

$('#bar_men_sep_line').mouseenter(function(){
	$('#men_pop_sep').show();
});
$('#bar_men_sep_line').mouseleave(function(){
	$('#men_pop_sep').hide();
});
$('#bar_women_sep_line').mouseenter(function(){
	$('#women_pop_sep').show();
});
$('#bar_women_sep_line').mouseleave(function(){
	$('#women_pop_sep').hide();
});

$('#bar_men_oct_line').mouseenter(function(){
	$('#men_pop_oct').show();
});
$('#bar_men_oct_line').mouseleave(function(){
	$('#men_pop_oct').hide();
});
$('#bar_women_oct_line').mouseenter(function(){
	$('#women_pop_oct').show();
});
$('#bar_women_oct_line').mouseleave(function(){
	$('#women_pop_oct').hide();
});

$('#bar_men_nov_line').mouseenter(function(){
	$('#men_pop_nov').show();
});
$('#bar_men_nov_line').mouseleave(function(){
	$('#men_pop_nov').hide();
});
$('#bar_women_nov_line').mouseenter(function(){
	$('#women_pop_nov').show();
});
$('#bar_women_nov_line').mouseleave(function(){
	$('#women_pop_nov').hide();
});

$('#bar_men_dec_line').mouseenter(function(){
	$('#men_pop_dec').show();
});
$('#bar_men_dec_line').mouseleave(function(){
	$('#men_pop_dec').hide();
});
$('#bar_women_dec_line').mouseenter(function(){
	$('#women_pop_dec').show();
});
$('#bar_women_dec_line').mouseleave(function(){
	$('#women_pop_dec').hide();
});