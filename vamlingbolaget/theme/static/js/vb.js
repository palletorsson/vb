
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

var initsize = function(){
    if($('#nosize')[0]) {
        var allsizes = $(".select_size");
        var some_size = Math.floor(allsizes.length/2)-1;
        if (some_size < 0) { some_size = 0; }
        console.log(allsizes[some_size].id)

        allsizes.each(function( value, index ) {
            if (this.id == parseInt(allsizes[some_size].id)) {
                $(this).addClass('size_active active');
                console.log(this, allsizes[some_size].id);
            }

        });
        var sellec = "#"+allsizes[some_size].id+".select_size";
        $(sellec).addClass('active');
            $(sellec).addClass('size_active');
        var sizeval = $("#size");
        sizeval.val(allsizes[some_size].id);

    }
};


var counter = 0;

$('#nosize').hide();

$("#addtocart").off('click').on({
    click:function(e) {
        var size_val = $('#size').val();
        if (size_val == ''){
          var size_val = $('#sizebargin').val();

        }
        console.log("check size", size_val)
        if (size_val == ''){
           $('.remove_on_size').addClass('add_size_message');
           $('#nosize').show();
           $('#nosize').delay(2000).fadeOut(3000);
      } else {
        e.stopPropagation();
        if(counter == 0){
            console.log("first when size ok")
            counter++;
            setTimeout(function(){counter = 0},2000)

            full = $('#add_or_edit').val();
            console.log(full);
            s_type = $('#s_type').val();
            console.log(s_type);
            console.log("add to cart");

            if (full == 'full') {
                var add_or_edit = 'full'
            }
            else {
                var add_or_edit = 'add';
            }
        	var sku_number = $('#sku_number').text(),
        		product_type = $('#product_type').text(),
        		quality = $(".quality").text(),
        		size_id = $('#size').val() || 3840,
        		article_id = $('#article_pk').val(),
                full_var = $('#full_var').val() || 0
        		quantity = $('#quantity').val(),
        		color = $('#color').val() || $('#color option:selected').val() || $('#hidden_colorpattern').val(),
        		the_price = $("#the_price").text(),
        		pattern = $('#pattern').val() || $('#pattern option:selected').val() || $('#hidden_colorpattern').val(),
        		color2 = 0,
        		pattern2 = 0;
                console.log(size_id)
        	if (sku_number == 9805) { //fill in proper article no for 2 patterned items
                if (full_var != 1) {
        		   color2 = $('#color2').val();
        		   pattern2 = $('#pattern2').val();
                }
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
                s_type: s_type,
        		csrfmiddlewaretoken: csrftoken,
        		cartitem_id: '1',
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



    			$("#updatecart").html( '<div class="card border-info mb-3" style="max-width: 12rem;"> <div class="card-body"> <h6 class="card-title">'+ widgetTextstart+ ' '+_.article +' </h6>' +
    				 ' <p class="card-text text-info">'+ widget_size +' </p>' +
                     ' <p class="card-text">'+ coltext +', '+ pattext +' </p>' +

    				 ' </div></div>').fadeIn();

    			$("#updatecart").delay(6000).fadeOut(3000).animate({
                      height:'0px'
                    });

        			var old_quantity = $("#widget_quantity").text();
        			var new_quantity = parseInt(quantity) + parseInt(old_quantity);
        			$('#widget_quantity').text(new_quantity);

        			var old_price = $("#widget_total").text();
        			var new_price = parseInt(the_price) + parseInt(old_price);
        			$('#widget_total').text(new_price);
                    $(".button_has_item").css({borderStyle: "groove", borderWidth: "2px", borderColor: "#ff0000"})

    		  }
    	   });
        }
    }
    }

});//end of click


$("#addtofullcart").off('click').on({

    click:function(e) {
        e.stopPropagation();
        if(counter == 0){
                console.log("addtofullcart")
            counter++;
            setTimeout(function(){counter = 0},2000)

            full = $('#add_or_edit').val();

            if (full == 'full') {
                var add_or_edit = 'full'
            }
            else {
                var add_or_edit = 'add';
            }

            var sku_number = $('#sku_number').text(),
                product_type = $('#product_type').text(),
                quality = $(".quality").text(),
                size_id = $('#size').val() || size_id_default,
                article_id = $('#article_pk').val(),
                mess = $('#id_message').text(),
                quantity = $('#quantity').val(),
                color = $('#color').val() || $('#color option:selected').val() || $('#hidden_colorpattern').val(),
                the_price = $("#the_price").text(),
                pattern = $('#pattern').val() || $('#pattern option:selected').val() || $('#hidden_colorpattern').val(),
                color2 = 0,
                pattern2 = 0;

            if (sku_number == 9805) { //fill in proper article no for 2 patterned items
                color2 = $('#color2').val();
                pattern2 = $('#pattern2').val();
            }

            $.ajax({
                type:"POST",
                url:"/cart/addtofullcart/",
                data: {
                article_sku: sku_number,
                color: color,
                color2: color2,
                pattern: pattern,
                pattern2: pattern2,
                size: size_id,
                csrfmiddlewaretoken: csrftoken,
                cartitem_id: '1',
                quantity: quantity,
                add_or_edit : add_or_edit,
                message: mess
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
                console.log(_.s_type)
             $("#updatecart").animate({
                      height:'200px'
                    });

                    $("#updatecart").html( '<div class="card border-info mb-3" style="max-width: 12rem;"> <div class="card-header"> '+ widgetTextstart+ ' '+_.article +' </div>' +
                    ' <div class="card-body text-info"> <p class="card-text">'+ widget_size +' </p>' +
                    ' <p class="card-text">'+ coltext +', '+ pattext +' </p>' +

                    ' </div></div></div>').fadeIn();

                $("#updatecart").delay(6000).fadeOut(3000).animate({
                      height:'0px'
                    });

                    var old_quantity = $("#widget_quantity").text();
                    var new_quantity = parseInt(quantity) + parseInt(old_quantity);
                    $('#widget_quantity').text(new_quantity);

                    var old_price = $("#widget_total").text();
                    var new_price = parseInt(the_price) + parseInt(old_price);
                    $('#widget_total').text(new_price);
                    $(".button_has_item").css({borderStyle: "groove", borderWidth: "2px", borderColor: "#ff0000"})

              }
           });
        }
    }
});//end of click

$(".variation_imgs").on( {

    'click': function(e) {

        e.stopPropagation();

        console.log("-----", this, e)

        var img = $(this).attr('src');

        console.log(img)

        $(".variation_img").attr("src", img)
        $(".variation_link").attr("href", img)
    },
    'contextmenu' : function(e) {
        console.log("......", this, e)
    }
});



$('#widget_size').filter(function () {
    var lang_text = $(this).text();
    if (lang_text != 'Storlek') {
       $('#ethics').parent().remove()
    }
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
			     $("#updatecart").html('<div class="card border-info mb-3" style="max-width: 12rem;"> <div class="card-body text-info"> <p class="card-text">  ' + article_etc + ' ' + article_size + '</p></div></div></div>').fadeIn();
            }
            else {
                $("#updatecart").html('<div class="card border-info mb-3" style="max-width: 12rem;"> <div class="card-body text-info"> <p class="card-text"> ' + msg + '</p></div></div></div>').fadeIn();
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
        product_type = $('#product_type') || 'none',
        cartitem_id = $('#cartitem_id').text(),
        quality = $(".quality").text() | 'none',
        size_id = $('#size option:selected').val() || size_id_default,
        article_id = $('#article_pk option:selected').val(),
        quantity = $('#quantiy_pk option:selected').val() || 1,
        color = $('#color option:selected').val() || $('#hidden_colorpattern').val() || 0;
    var pattern= $('#pattern option:selected').val() || $('#hidden_colorpattern').val() || 0;
    var color2 = 0;
    var pattern2 = 0;

        if(sku_number == 9805){ //fill in proper article no for 2 patterned items
            color2 = $('#color2').val(),
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


$('.abouts').filter(function () {
    var about = $("#about").text().trim();
    console.log(about);
    if(about == 'Om oss') {
        remove = false;
    } else if (about == 'About') {
        remove = false;
    } else {
        remove = true;
    }
    if (remove == true) {
        console.log("remove");
        $('.onlysv').remove();
    } else {
        console.log("keep");
    }
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


var path = location.pathname
var link = $('a[href="'+window.location.pathname+'"] span')

if ($(link).hasClass("nolink")) {
    console.log("no link");
} else {
    link.addClass('active-link');

}

var $allVideos = $(".vimeoVid"),
$fluidEl = $(".vimeoDiv");

$allVideos.each(function() {

  $(this)
    // jQuery .data does not work on object/embed elements
    .attr('data-aspectRatio', this.height / this.width)
    .removeAttr('height')
    .removeAttr('width');

});

$(window).resize(function() {

  var newWidth = $fluidEl.width();
  if (newWidth > 500) {
    newWidth = Math.floor(newWidth * 0.8);
  }
  $allVideos.each(function() {

    var $el = $(this);
    $el
        .width(newWidth)
        .height(newWidth * $el.attr('data-aspectRatio'));

  });
  console.log("resize ", newWidth, $allVideos);

}).resize();

$('body input[type=text]').addClass('form-control');

window.onscroll = function (e) {

    console.log("hide scroll");
    $('.scrolldown').hide();
}

if (window.location.pathname == "/products/cut/") {
    var text_size = $("#source_size").text();
    $("#target_size").text(text_size);
    var sq = $("#source_squality").text()
    $("#target_squality").text(sq);
    var text_choose = $("#source_choose").text();
    $("#target_choose").text(text_choose);
    var text_thisn = $("#source_thisn").text();
    $("#target_thisn").text(text_thisn);
    var text_thist = $("#source_thist").text();
    $("#target_thist").text(text_thist);
    var text_fabric = $("#source_fabric").text();
    $("#target_fabric").text(text_fabric);

    var text_choosemodel = $("#source_choosemodel").text();
    $("#target_choosemodel").text(text_choosemodel);
    var text_choosefabric = $("#source_choosefabric").text();
    $("#target_choosefabric").text(text_choosefabric);
    var text_choosesize = $("#source_choosesize").text();
    $("#target_choosesize").text(text_choosesize);

    var text_art = $("#source_art").text();
    $("#target_art").text(text_art);

    var text_choosen = $("#source_choosen").text();
    $("#target_choosen").text(text_choosen);

    var text_sum = $("#source_sum").text();
    $("#target_sum").text(text_sum);

    var text_makechoose = $("#source_makechoose").text();
    $("#target_makechoose").text(text_makechoose);

    var text_add = $("#source_add").text();
    $("#target_add").text(text_add);
}

var set_first_page = function(){
     var wheight = $(window).height(),
     wwidth = $(window).width(),
     fullheight = wheight;
     img_heigth = $('.halffullscreen img').height()


        $('.spanfullscreen').css({'width':$(window).width(),'background-color':'#fff','margin':0, height:img_heigth +'px', 'overflow':'hidden', 'padding':0 });
        $('.halffullscreen').css({'float':'left','width':($(window).width())/2, 'background-color':'#fff','margin':0, 'height': img_heigth +'px', 'overflow':'hidden', 'padding':0 });
        $('.halffullscreen img').css({'width':(($(window).width())/2), 'height': 'auto', 'margin':0, 'padding-top': '80px' });
        $('.spanfullscreen img').css({'width':($(window).width()), 'height': 'auto', 'margin':0, 'padding':0, 'padding-top': '80px' });
        $('.spanfullscreenminus img').css({'width':($(window).width()), 'height': 'auto', 'margin':0, 'padding':0, 'padding-top': '0px' });

    if (wwidth < 440){
        var imgs = $('.spanfullscreen').find('img');

        $('.spanfullscreen').height(($(window).height())/2.5);
    }


    $('.carousel-control').show()
}


$('#continue_payment').click(function(e) {
    console.log("overlay");
    var overlay = $('<div id="overlay" ></div>');
    overlay.appendTo(document.body);
});

$( window ).resize(function() {
    set_first_page();
});

$('#sms-checkbox').click(function () {
	var sms_val = $('input[name=sms]').val()
    if (sms_val == 'no') {
	    $('input[name=sms]').val('yes')
    } else {
	    $('input[name=sms]').val('no')
	}

});

$('.change_lang').click(function(e){
    e.stopPropagation();
    var val = $(this).attr('id');
    console.log("lang", val);
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
      var img_text = color_name + ' ' +pattern_name+ ' ';
	  var image_url = '<img src="/media/uploads/120/'+color+'f_'+pattern+'m.jpg" class="img_selected" width="180"> <br />';

      if ($(this).hasClass("inside")) {
		$("#selectedpatternandcolor_inside").html(image_url);
        $('input[name="pattern_2"]').val(pattern);
        $('input[name="color_2"]').val(color);
	  } else {
	   $(".selectedpatternandcolor").html(image_url);
	   $(".selectedpatternandcolor_text").html(img_text);
       $('input[name="pattern"]').val(pattern);
       $('input[name="color"]').val(color);
	  }

    });

    $(".select_size").click(function(e) {
        e.stopPropagation();
        var size_id = this.id;
        var ok = $('input[name="size"]').val(size_id);;
        $('.select_size').removeClass('size_active');
        $('.select_size').removeClass('active');
        $('.size_active').removeClass('size_active');
        $('.active').removeClass('active');
        $(".remove_on_size").remove();
        var $this = $(this);

        if (!$this.hasClass('size_active')) {
            $this.addClass('size_active');
            $this.addClass('active');
        }

        var a = $this.data('size');

        if (a < 1) {

            $('.stock_text_no').removeClass('hidden');
            $('.stock_text_yes').addClass('hidden');
        } else if (a == 'none') {
            console.log(a)
        } else {
            $('.stock_text_yes').removeClass('hidden');
            $('.stock_text_no').addClass('hidden');
        }
        e.preventDefault();
    });

    $(".select_quantity").click(function(e) {

      e.stopPropagation();
      var quantity_id = this.id;
      var ok = $('input[name="quantity"]').val(quantity_id);;

      $('.select_quantity').removeClass('size_active');
      var $this = $(this);
    if (!$this.hasClass('size_active')) {
        $this.addClass('size_active');
    }



    e.preventDefault();
    });

    $(".mainnav li a").click(function(e) {
          console.log(toString(window.location))
      var $this = $(this);


    $(".mainnav li a").removeClass('link_active');
     var $this = $(this);
    if (!$this.hasClass('link_active')) {
        $this.addClass('link_active');
    }

    });
    var $klarna = $('#klarna'),
        $card = $('#card'),
        $post = $('#post');


    var val_check =  $("#id_first_name").val();
    if (val_check == 'Klarna') {
        var adress_div = $('#adress_form');
        adress_div.hide();
        $('input[name="paymentmethod"]').val('K');
        $('input[type="text"]').val('');
        $('input[type="email"]').val('');
        var payment_txt = $("input[value='klarna']").parent().text()
        $('#continue_payment').val(payment_txt);
    }


    $(".radiopay").on({
        click: function(e) {
            e.stopPropagation();
            $('input[name="payment"]').prop('checked', false);
            $(this).find("input[type=radio]").prop("checked", true)
            var pay_val = $(this).find("input[type=radio]").val()
            $('.paymenttext').each(function() {
                $(this).removeClass('active');
            });
            $('#'+pay_val).addClass('active');
            payment_txt = $.trim($(this).text());
            $('#continue_payment').val(payment_txt);

            if (pay_val == 'klarna') {
                var adress_div = $('#adress_form');
                $('.hidden_adress_form').html(adress_div.html())
                adress_div.fadeOut(500);
                adress_div.animate({ height: "0px" }, 700)
                adress_div.delay(200).hide();
                $('input[name="paymentmethod"]').val('K');
                $('input[type="text"]').val('Klarna');
                $('input[id="id_email"]').val('temp@klarna.com');
            } else {
                var form_hidden = $('.hidden_adress_form')
                if (form_hidden.html().length > 1) {
                    $('#adress_form').html(form_hidden.html());
                    $('#adress_form').fadeIn(300);
                    $('input[type="text"]').val();
                    $('input[type="email"]').val();
                }


            }
           $(this).focus();
           if (pay_val == 'card') {
                $('input[name="paymentmethod"]').val('C');

            } else if (pay_val == 'post') {

                $('input[name="paymentmethod"]').val('P');

            } else {
                $('input[name="paymentmethod"]').val('K');

            }
        },
        mouseover: function() {
            var targetDiv = this.id;

            if (targetDiv == 'K') {
                $klarna.removeClass('hidden');
                $card.addClass('hidden');
                $post.addClass('hidden');
            } else if (targetDiv == 'C') {
                $card.removeClass('hidden');
                $klarna.addClass('hidden');
                $post.addClass('hidden');
            } else {
                $post.removeClass('hidden');
                $klarna.addClass('hidden');
                $card.addClass('hidden');
            }

        },
        mouseout:function(){
            var targetDiv = this.id;
            $klarna.addClass('hidden');
            $card.addClass('hidden');
            $post.addClass('hidden');

            $('.paymenttext').each(function() {
                if ($(this).hasClass('active')) {
                    $(this).removeClass('hidden');
                }
            });

        }
    });


    $(".showexpanded").click(function(e) {
        pc_sellection = $('#pc_sellection');
        e.stopPropagation();
        $(".showcommon").removeClass('hidden');
        $('.pc_expanded').removeClass('hidden');
        $('.showexpanded').addClass('hidden');
        $('.pc_common').addClass('hidden');
        pc_sellection.val('expanded')
    });


    $(".showcommon").click(function(e) {
        pc_sellection = $('#pc_sellection');
        e.stopPropagation();
        $(".showexpanded").removeClass('hidden');
        $('.pc_common').removeClass('hidden');
        $('.showcommon').addClass('hidden');
        $('.pc_expanded').addClass('hidden');
        pc_sellection.val('common');
    });

      var size_id = this.id;
      var ok = $('input[name="size"]').val(size_id);;

      $('.select_size').removeClass('size_active');
      $('.select_size').removeClass('active');
      var $this = $(this);
    if (!$this.hasClass('active')) {
        $this.addClass('size_active');

    }

    var a = $this.data('size');


    $('#myTab a').click(function (e) {

    // payment method logic

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

    // serach order by order id

    $("#search_order").click(function(e) {
        var order_id = $('#order_id').val();
        console.log("search_order ", order_id);
        window.location = '/orders/order/'+order_id+"/"
    });

    $("#search_name").click(function(e) {
        var order_name = $('#order_name').val();
        console.log("search_name ", order_name);
        window.location = '/orders/ordersByName/'+order_name+"/"
    });


    // for pacsoft autoaddress
	$(".address_button").click(function() {

		var input_address = $('.input_address').val();
        console.log(input_address);
		$("#target_address").text(input_address);

	});

    $('#Service').on('change', function () {
          var extra = $(this).val();
          var weight = $('#weight').val();
          if (weight == '') {
            weight = 1000;
          }
          var base_url = $('#urlbase').html();
          var final_url = base_url + extra + "/" + weight + "/";
          $('#target_url').attr('href', final_url);
          return true;
      });

    $('input[name=weight]').on('change', function () {
          var weight = $(this).val();

          if (weight == '') {
            weight = 1000;
          }


          var base_url = $('#urlbase').html();

          var extra = $("#Service :selected").val();
          var final_url = base_url + extra + "/" + weight + "/";

          $('#target_url').attr('href', final_url);
          return true;
      });

function scroll_init() {
    window.addEventListener('scroll', function(e){
        var distanceY = window.pageYOffset || document.documentElement.scrollTop;
        var shrinkOn = 200;
        console.log();
        if (document.documentElement.scrollTop > shrinkOn) {
            $('.menu_container').animate({ height: "50px" }, 500 ).addClass('shriked');
            $('.vb_logo').animate({ width: "100px" }, 500 );
            $('.main_nav').animate({ top: "-11px" }, 500, function() {
                $('.navbar-brand').hide();
                //$('.midhead').hide();
            });
        }  else {
           if (document.documentElement.scrollTop < shrinkOn+1000 && $('.menu_container').hasClass('shriked')) {

              $('.navbar-brand').show();
               // $('.midhead').show();
              $('.menu_container').animate({ height: "160px" }, 500 );
              $('.vb_logo').animate({ width: "120px" }, 500 );
              $('.main_nav').animate({ top: "80px" }, 500, function() {
                $('.menu_container').removeClass('shriked');
            });
              console.log(distanceY, shrinkOn)
           }
        }

    });
}

initsize();



}); // --- end document readyfunction
