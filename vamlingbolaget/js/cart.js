
$(function(){

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
})

    $('.icon-minus').click(function(e){
        e.stopPropagation();
        e.preventDefault();
        if(confirm('Vill du ta bort denna post?')){
                var id = $(this).attr('id');
                $.ajax({
                    url: '/cart/removefromcart/'+id,
                    csrfmiddlewaretoken: csrftoken,
                    contentType: "application/json",
                    success: function( data ) {
                        if(data.totalprice != 0){
                            $('#totalprice').html(data.totalprice);
                        }else{
                            $('.totalprice').html('Du har tömt din varukorg <a href="/products/">fortsätt att utforska vårt utbud</a>');
                            $('#totalprice').html(data.totalprice);
                        }
                        $('#'+id).closest('tr').remove();
                    }
            })


        }
    });
/*
    $('.icon-edit').click(function(e){
        e.stopPropagation();
        e.preventDefault();
        if(confirm('Vill du ta editera denna post?')){
            var id = $(this).attr('id');
            $.ajax({
                url: '/cart/editcart/'+id,
                csrfmiddlewaretoken: csrftoken,
                contentType: "application/json",
                success: function( data ) {
                    console.log(data);
                }
            })


        }
    });
*/

})
