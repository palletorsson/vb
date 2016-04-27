
$('document').ready(function(){

// setting up CSRF
// using jQuery,
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
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
}); // --- CSRF end

// --- setting up cart-widget
// add to cart - unika och gemensamma taggar

var size_id_default = 1;

if($('#hidden_colorpattern')){
    var first_color_id = "{{ product.color.order }}";
    $('#hidden_colorpattern').val(first_color_id);
    $('input[name=radio]').change(function () {
        $('#hidden_colorpattern').val(this.value);
    });
}

$(".changonselect").change(function () {

$('#fadeifchangeorder').fadeTo(500,0.6);

var article_name =  $('#articlename').text();
var str = "Beställ "+article_name+ " i ",
    folder = "/media/uploads/120/",
    img = "";

var once = 1,
		img2,
		img,
		pattern2_id = $("#pattern2").val() || null;

$(".changonselect option:selected").each(function () {
	str += $(this).text() + " ";
	if (once == 1) {
		str += " och ";
    }

    once = 2;

    var pattern_id = $("#pattern").val(),
			color_id = $("#color").val(),
			size_id = $("#size").val(),
			color2_id = $("#color2").val() || null;
			
		img = folder+color_id+"f_"+pattern_id+"m.jpg";
		
		if(pattern2_id){
			img2 = folder+color2_id+"f_"+pattern2_id+"m.jpg";
		}
});

$("#select_text").text(str);

$("#pattern_color_image").attr("src", img);
	if(pattern2_id){
		$("#pattern_color_image2").attr("src", img2);
	}

});



$("#addtocart").click(function() {


	var add_or_edit = 'add';

	var sku_number = $('#sku_number').text(),
		product_type = $('#product_type').text(),
		quality = $(".quality").text(),
		size_id = $('#size').val() || size_id_default,
		article_id = $('#article_pk').val(),
		quantity = $('#quantity').val(),
		color = $('#color').val() || $('#color option:selected').val() || $('#hidden_colorpattern').val(),
		the_price = $("#the_price").text(),
		pattern = $('#pattern').val() || $('#pattern option:selected').val() || $('#hidden_colorpattern').val(),
		color2 = 0,
		pattern2 = 0;

	console.log(sku_number, product_type, quality, size_id + "art_n" + article_id, quantity, color, the_price, pattern) 

	if (sku_number == 9805) { //fill in proper article no for 2 patterned items
		color2 = $('#color2').val();
		pattern2 = $('#pattern2').val();
	}

	$.ajax({
		type:"POST",
		url:"/cart/addtocart/",
		data: {
		article_sku: sku_number,
		color: color,
		color2: color2,
		pattern: pattern,
		pattern2: pattern2,
		size: size_id,
		csrfmiddlewaretoken: csrftoken,
		cartitem_id: '0',
		quantity: quantity,
		add_or_edit : add_or_edit
		},
		
		success: function(data){
		var msg = data.message.msg,
			_ = data.cartitem;
		var widgetTextstart = $('#widget_text_start').text();
		var widgetSize = $('#widget_size').text();
		var widgetExist = $('#widget_exist').text();
		var widgetTextend = $('#widget_text_end').text();
		var widgetTextin = $('#widget_text_in').text();
        var widget_size = $('.size_active').text();
		if(color2 === 0) {
			var coltext = _.color,
			pattext = _.pattern;
		} else {
			var coltext = _.color +' / '+_.color2,
			pattext = _.pattern +' / '+_.pattern2;

			}

		 $("#updatecart").animate({
		          height:'200px'
		        });

			$("#updatecart").html( '<hr> <li> <strong> '+ widgetTextstart+ ' </strong></li><hr><li>'+_.article +' </li>' +
				 '<li> - '+ widget_size +' </li>' +
                 '<li> '+ coltext +', '+ pattext +' </li>' +
				
				 ' <div>').fadeIn();

			$("#updatecart").delay(6000).fadeOut(3000).animate({
                  height:'0px'
                });;

			var old_quantity = $("#widget_quantity").text();
			var new_quantity = parseInt(quantity) + parseInt(old_quantity);
			$('#widget_quantity').text(new_quantity);

			var old_price = $("#widget_total").text();
			var new_price = parseInt(the_price) + parseInt(old_price);
			$('#widget_total').text(new_price);

		}
	});

});

$("#addreatocart").click(function() {
	var item = $('#rea_pk').val();
	the_price = $("#the_price").text(),
    $.ajax({
        type:"POST",
        url:"/cart/addrea/",
        data: {
           item : item
        },
        success: function(data){
                 $("#updatecart").animate({
                  height:'200px'
                });

            var article_etc = $('#article_etc').text();
            var article_size = $('#article_size').text();
            console.dir(data); 
            var msg = data.message.msg,
                _ = data.cartitem;

            if (msg != "Fyndet finns redan ") {                
			     $("#updatecart").html('<hr><li> <strong> + </strong></li><hr> <li> ' + article_etc + '</li><li> ' + article_size + '</li>').fadeIn();
            } 
            else {
                $("#updatecart").html('<hr><li> <strong> - </strong></li><hr> <li> ' + msg + '</li>').fadeIn();
            }

            if (msg != "Fyndet finns redan ") { 
			    var old_quantity = $("#widget_quantity").text();
				var new_quantity = 1 + parseInt(old_quantity);
				$('#widget_quantity').text(new_quantity);

				var old_price = $("#widget_total").text();
				var new_price = parseInt(the_price) + parseInt(old_price);

				$('#widget_total').text(new_price);
			}

            $("#updatecart").delay(6000).fadeOut(3000).animate({
                  height:'0px'
                });;
        }
    });
});
// edit cart

$(".changonselectupdate").change(function () {
    var add_or_edit = 'edit';
    var article_update = $('#articleupdate').text();
    var str = "Uppdatera "+article_update+ " i ",
            folder = "/media/uploads/120/",
            img = "";

    var once = 1,
            img,
            img2,
            pattern2_id = $("#pattern2").val() || null;

    $(".changonselectupdate option:selected").each(function () {
        str += $(this).text() + " ";
        if (once == 1) {
            str += " , ";
        }
        once = 2;

        var pattern_id = $("#pattern").val(),
                color_id = $("#color").val(),
                size_id = $("#size").val(),
                color2_id = $("#color2").val() || null;

        img = folder+color_id+"f_"+pattern_id+"m.jpg";

        if(pattern2_id){
            img2 = folder+color2_id+"f_"+pattern2_id+"m.jpg";
        }
    });

    $("#changetextupdate").text(str);
    $("#pattern_color_image").attr("src", img);
    if(pattern2_id){
        $("#pattern_color_image2").attr("src", img2);
    }
});




$("#changecart").click(function() {

    var add_or_edit = 'edit';
    var sku_number = $('.sku_number').text(),
        product_type = $('#product_type'),
        cartitem_id = $('#cartitem_id').text(),
        quality = $(".quality").text(),
        size_id = $('#size option:selected').val() || size_id_default,
        article_id = $('#article_pk option:selected').val(),
        quantity = $('#quantiy_pk option:selected').val(),
        color = $('#color option:selected').val() || $('#hidden_colorpattern').val();
    var pattern= $('#pattern option:selected').val() || $('#hidden_colorpattern').val();
    var color2 = 0;
    var pattern2 = 0;

        if(sku_number == 9805){ //fill in proper article no for 2 patterned items
            color2 = $('#color2').val(),
            pattern2 = $('#pattern2').val();
        }
    console.log(sku_number)
    $.ajax({
        type:"POST",
        url:"/cart/addtocart/",
        data: {
            article_sku: sku_number,
            color: color,
            color2: color2,
            pattern: pattern,
            pattern2: pattern2,
            size: size_id,
            csrfmiddlewaretoken: csrftoken,
            cartitem_id: cartitem_id,
            quantity: quantity,
            add_or_edit : add_or_edit
        },
        success: function(data){
            window.location.href = "/cart/show/"
        }
    });

    });


// remove cart item

$('.icon-minus').click(function(e){
    e.stopPropagation();
    e.preventDefault();
    var rm_message = $('#widget_text_remove').text();
    if(confirm(rm_message)){
            var id = $(this).attr('id'),
                my_url = $(this).parent('a').attr('href');
            $.ajax({
                url: my_url,
                csrfmiddlewaretoken: csrftoken,
                contentType: "application/json",
                success: function( data ) {
                    if(data.totalprice != 0){
                        $('#totalprice').html(data.totalprice);
                    }else{
                        $('.totalprice').html('Du har tömt din varukorg <a href="/products/">fortsätt att utforska vårt utbud</a>');
                        $('#totalprice').html(data.totalprice);
                        $('#handling').parent().remove();
                        $('button').hide();
                    }
                    $('#'+id).closest('tr').remove();
                    window.location.href = "/cart/show/"
                }
        })


    }
});

$('#vocher-plus').click(function(e){
    e.stopPropagation();
    e.preventDefault();
    var key = $('#id_voucher').val();
    $('#id_voucher').val("");
    my_url = "/cart/voucher/" + key;
            $.ajax({
                url: my_url,
                csrfmiddlewaretoken: csrftoken,
                contentType: "application/json",
                success: function( data ) {
					window.location.href = "/cart/show/"
                }

        })
 
});


// --- setup welcome page animation

var changesrc = function(me, from, to){
    var oldsrc = me.attr('src'),
        newsrc = oldsrc.replace(from,to);
    return newsrc;
}

var initgallery = function(){
    $('.enlarge').hover(function(){
         $(this).attr('src', changesrc($(this), 'thumbnail','small'))
    }, function(){
         $(this).attr('src', changesrc($(this), 'small', 'thumbnail'))
    });

    $('.isfeatured').hover(function(){
         $(this).attr('src', changesrc($(this), 'medium','medium'))
    }, function(){
         $(this).attr('src', changesrc($(this), 'medium','thumbnail'))
         $(this).removeClass('isfeatured').addClass('enlarge');
         initgallery();
    });
}

//initgallery();

/*
 * Overlay for gallery feature images that
 * dynamically calculates size of image.
 * The siblings are the feature images, perform check when these are loaded
 */

$('.overlay').each(function(){
    var me = $(this);
    console.log($(this).parent().closest('div'));
    $(this).siblings().load(function(){
        var width = $(this).parent().css('width'),
            pos = $(this).parent().offset();
        me.css({'width': width, 'left':pos.left, 'top':pos.top, 'height': '20px', 'background-color':'#000', 'color':'#fff'});
    })
});

/*
 * First-page spans whole screen, set the div-width and height dynamically based on viewport-width
 * and adjust the image heights accordingly, remove space
 */


var set_first_page = function(){
     var wheight = $(window).height(),
     wwidth = $(window).width(),
     fullheight = wheight+200;


        $('.spanfullscreen').css({'width':$(window).width(), 'background-color':'#fff','margin':0, 'height': fullheight +'px', 'overflow':'hidden', 'padding':0 });
        $('.halffullscreen').css({'float':'left','width':($(window).width())/2, 'background-color':'#fff','margin':0, 'height': fullheight +'px', 'overflow':'hidden', 'padding':0 });
        $('.halffullscreen img').css({'width':(($(window).width())/2), 'height': 'auto', 'margin':0, 'padding':0 });
        $('.spanfullscreen img').css({'width':($(window).width()), 'height': 'auto', 'margin':0, 'padding':0, 'margin-top': '80px'});

    if (wwidth < 440){
        var imgs = $('.spanfullscreen').find('img');

        $('.spanfullscreen').height(($(window).height())/2.5);
    }


    $('.carousel-control').show()
}

$('#sms-checkbox').click(function () {
	var sms_val = $('input[name=sms]').val()
    if (sms_val == 'no') {
	    $('input[name=sms]').val('yes')
    } else {
	    $('input[name=sms]').val('no')
	}
 
});

$('.change_lang').click(function(){
    var val = $(this).attr('id');
    $('input[name=language]').val(val)
    $('form#lang').submit();
});

set_first_page();

// --- end of welcome page animation
// choose color and pattern logict
    var open = 0;

    // $(".color_and_pattern_choose").hide();

     $(".open_dialog").click(function(e) {
        $(".color_and_pattern_choose").toggle(200);
        if (open == 0) {
            $(".open_dialog").text('Stäng fler färger och mönster');
            open = 1;
        } else {
            $(".open_dialog").text('Fler färger och mönster');
            open = 0;
        }
     });

    $(".pattern_color_image").click(function(e) {
      e.stopPropagation();
      var colorandpattern = this.id.split("_");
      var color = colorandpattern[0];
      var pattern = colorandpattern[1];
      var color_name = colorandpattern[2];
      var pattern_name = colorandpattern[3];
	  var image_url = '<img src="/media/uploads/120/'+color+'f_'+pattern+'m.jpg" class="img_selected" width="120"> <br />'+ color_name + ' ' +pattern_name+ ' ';
      var txt = color_name + ' ' +pattern_name 
      
      if ($(this).hasClass("inside")) {
		$("#selectedpatternandcolor_inside").html(image_url);
        $('input[name="pattern_2"]').val(pattern);
        $('input[name="color_2"]').val(color);
	  } else {
	   $(".selectedpatternandcolor").html(image_url);
	   $(".selectedpatternandcolor_text").html(txt);
       $('input[name="pattern"]').val(pattern);
       $('input[name="color"]').val(color);
	  }

    });


    $(".select_size").click(function(e) {
      e.stopPropagation();
      var size_id = this.id; 
      var ok = $('input[name="size"]').val(size_id);;
    
	  $('.select_size').removeClass('size_active');
  var $this = $(this);
    if (!$this.hasClass('size_active')) {
        $this.addClass('size_active');
    }
    e.preventDefault();
    });


    // payment method logic
    $('#myTab a').click(function (e) {

        e.preventDefault();
        $(this).tab('show');
        

		$('input[name="paymentmethod"]').val(this.id);
		
        handel_el = $('#handling'); 
        handel_el_value = handel_el.text().trim(); 

        sum = $('#totalprice');
        sum_el = $('#totalprice')
        sum_value = sum_el.html().trim(); 
       
        sum_value = sum_value.substring(0, sum_value.length - 4); 
        
        if (this.id == 'P') {
			if(parseInt(handel_el_value) == 80) { 
				handel_el.html(parseInt(handel_el_value)+40)
				sum_el.html((parseInt(sum_value)+40) + ' SEK')
			}
		} else {
			if(parseInt(handel_el_value) == 120) { 
				handel_el.html(parseInt(handel_el_value)-40)
				sum_el.html((parseInt(sum_value)-40) + ' SEK')
			}
		}
    });

    // for pacsoft autoaddress 
	$(".address_button").click(function() {

		var input_address = $('.input_address').val();
        console.log(input_address); 
		$("#target_address").text(input_address); 

	}); 


}); // --- end document readyfunction
