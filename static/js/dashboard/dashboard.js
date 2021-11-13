var win_height = $(window).height();
$('.dashboard-main-banner').height(win_height);
$('.dashboard-side-banner').height(win_height);
var head_height = $('.dashboard-head-banner').height();
var r_height = win_height - head_height;
$('.dashboard-banner').height(r_height);

var $scrollable  = $(".dashboard-banner"),
    $scrollbar   = $(".scrollbar"),
    height       = $scrollable.outerHeight(true),    // visible height
    scrollHeight = $scrollable.prop("scrollHeight"), // total height
    barHeight    = height * height / scrollHeight;   // Scrollbar height!

// Scrollbar drag:
$scrollbar.height( barHeight ).draggable({
  axis : "y",
  containment : "dashboard-main-banner", 
  drag: function(e, ui) {
    $scrollable.scrollTop( scrollHeight / height * ui.position.top  );
  }
}); 

// Element scroll:
$scrollable.on("scroll", function() {
	var scroll = $scrollable.scrollTop();
  $scrollbar.css({top: $scrollable.scrollTop() / height * barHeight });
  if(scroll != 0){
  	$scrollbar.css({"opacity": "1"});
  }else{
  	$scrollbar.css({"opacity": "0"});
  }
});

$('#notify-dropdown').on('click', function(){
  $('#notification_dropdown').load("/dashboard/o-notification/");
});
$('#msg-dropdown').on('click', function(){
  $('#message_dropdown').load("/dashboard/m-notification/");
});


