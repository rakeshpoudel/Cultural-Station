const user_input = $("#order_search")
// const search_icon = $('#search-icon')
const artists_div = $('.result_cover')
const endpoint = '/dashboard/search-order/'
const delay_by_in_ms = 100
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            artists_div.promise().then(() => {
                // replace the HTML contents
                artists_div.html(response['html_from_view'])
                // fade-in the div with new contents
                // artists_div.fadeTo('fast', 1)
                // stop animating search icon
                // search_icon.removeClass('blink')
            })
        })
}


user_input.on('keyup', function () {


    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }

    // start animating the search icon with the CSS class
    // search_icon.addClass('blink')

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    var val1 = $(this).val();
    if(val1 != ''){
        $('.result_order').show();
    }else{
        $('.result_order').hide();
    }
    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
});



const user_input2 = $("#order_search_com")
// const search_icon = $('#search-icon')
const artists_div2 = $('.result_cover2')
const endpoint2 = '/dashboard/search-order-complete/'
const delay_by_in_ms2 = 100
let scheduled_function2 = false

let ajax_call2 = function (endpoint2, request_parameters) {
    $.getJSON(endpoint2, request_parameters)
        .done(response => {
            // fade out the artists_div, then:
            artists_div2.promise().then(() => {
                // replace the HTML contents
                artists_div2.html(response['html_from_view'])
                // fade-in the div with new contents
                // artists_div.fadeTo('fast', 1)
                // stop animating search icon
                // search_icon.removeClass('blink')
            })
        })
}


user_input2.on('keyup', function () {


    const request_parameters = {
        q: $(this).val() // value of user_input: the HTML element with ID user-input
    }

    // start animating the search icon with the CSS class
    // search_icon.addClass('blink')

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function2) {
        clearTimeout(scheduled_function2)
    }

    var val2 = $(this).val();
    if(val2 != ''){
        $('.result_order2').show();
    }else{
        $('.result_order2').hide();
    }
    // setTimeout returns the ID of the function to be executed
    scheduled_function2 = setTimeout(ajax_call2, delay_by_in_ms2, endpoint2, request_parameters)
})