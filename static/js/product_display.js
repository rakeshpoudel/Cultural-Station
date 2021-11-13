
//disabling checkbox-------------
var c_len = $('.choice_check:checked').length;

if(c_len == 0){
    $('.choice_check').attr('disabled', true);
}
//=======================================

//(function($) {
//    $.fn.clickToggle = function(func1, func2) {
//        var funcs = [func1, func2];
//        this.data('toggleclicked', 0);
//        this.click(function() {
//            var data = $(this).data();
//            var tc = data.toggleclicked;
//            $.proxy(funcs[tc], this)();
//            data.toggleclicked = (tc + 1) % 2;
//        });
//        return this;
//    };
//}(jQuery));

//removing space------------------
    $('.choice_check').attr("id", function(_, id) {
    return id.replace(/ /g, '');
});
//=============================

//var c = $('.choice_check1:last').attr("id");
//console.log(c);
//$(function(){
//    $('.click_cat').val(function(_, v){
//     return v.replace(/\s+/g, '');
//    });
//});

var cat_val = $('.click_cat').val();
c_val = cat_val.replace(/\s+/g, '');
var gender_val = $('.click_gender').val();
var tradition_val = $('.click_tradition').val();
$('#check' + c_val).prop('checked', true);
if(gender_val == 'men'){
    if(cat_val == 'traditional'){
        $('#checkmen' + cat_val).prop('checked', true);
        $('.men_tradition').show();
        $('.chevron_icon_cat1').css({"transform": "rotateZ(180deg)"});
    }else{
        $('#checkmen' + cat_val).prop('checked', true);
    }
    if(tradition_val == 'traditional'){
        $('.men_tradition').show();
        $('.chevron_icon_cat1').css({"transform": "rotateZ(180deg)"});
    }
}
if(gender_val == 'women'){
    if(cat_val == 'traditional'){
        $('#checkwomen' + cat_val).prop('checked', true);
        $('.women_tradition').show();
        $('.chevron_icon_cat2').css({"transform": "rotateZ(180deg)"});
    }else{
        $('#checkwomen' + cat_val).prop('checked', true);
    }
    if(tradition_val == 'traditional'){
        $('.women_tradition').show();
        $('.chevron_icon_cat2').css({"transform": "rotateZ(180deg)"});
    }
}


jQuery.fn.clickToggle = function(a, b) {
  return this.on("click", function(ev) { [b, a][this.$_io ^= 1].call(this, ev) })
};

$('.category_sub_header1').clickToggle(function(){
if(tradition_val == 'traditional' || cat_val == 'traditional'){
    if(gender_val=='men'){
        $('.men_tradition').slideUp(200);
        $('.chevron_icon_cat1').css({"transform": "rotateZ(0deg)"});
    }else{
        $('.men_tradition').slideDown(200);
        $('.chevron_icon_cat1').css({"transform": "rotateZ(180deg)"});
    }
}else{
        $('.men_tradition').slideDown(200);
        $('.chevron_icon_cat1').css({"transform": "rotateZ(180deg)"});
    }
},
function(){
if(tradition_val == 'traditional' || cat_val == 'traditional'){
    if(gender_val=='men'){
        $('.men_tradition').slideDown(200);
        $('.chevron_icon_cat1').css({"transform": "rotateZ(180deg)"});
    }else{
        $('.men_tradition').slideUp(200);
        $('.chevron_icon_cat1').css({"transform": "rotateZ(0deg)"});
    }
}else{
        $('.men_tradition').slideUp(200);
        $('.chevron_icon_cat1').css({"transform": "rotateZ(0deg)"});
    }
});
$('.category_sub_header2').clickToggle(function(){
if(tradition_val == 'traditional' || cat_val == 'traditional'){
    if(gender_val=='women'){
        $('.women_tradition').slideUp(200);
        $('.chevron_icon_cat2').css({"transform": "rotateZ(0deg)"});
    }else{
        $('.women_tradition').slideDown(200);
        $('.chevron_icon_cat2').css({"transform": "rotateZ(180deg)"});
    }
}else{
        $('.women_tradition').slideDown(200);
        $('.chevron_icon_cat2').css({"transform": "rotateZ(180deg)"});
    }
},
function(){
if(tradition_val == 'traditional' || cat_val == 'traditional'){
    if(gender_val=='women'){
        $('.women_tradition').slideDown(200);
        $('.chevron_icon_cat2').css({"transform": "rotateZ(180deg)"});
    }else{
        $('.women_tradition').slideUp(200);
        $('.chevron_icon_cat2').css({"transform": "rotateZ(0deg)"});
    }
}else{
        $('.women_tradition').slideUp(200);
        $('.chevron_icon_cat2').css({"transform": "rotateZ(0deg)"});
    }
});

$('.cat_choice').click(function(){
    $('.display_cover').show();
});