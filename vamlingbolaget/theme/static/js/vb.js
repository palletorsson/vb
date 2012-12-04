/*
//en instans
CartItemModel = Backbone.Tastypie.Model.extend({
    urlRoot: '/api/cart/cartitem/',
    defaults: {
        'label': 'no name yet'
    }
});

//lista av instanser
CartItemCollection = Backbone.Tastypie.Collection.extend({
    urlRoot: '/api/cart/cartitem/',
    model: CartItemModel
})

*/

$('document').ready(function(){

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
            console.log($(this).parent().closest('div'));
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
            fullheight = wheight-130;
        $('.spanfullscreen').css({'width':$(window).width(), 'background-color':'#fff','margin':0, 'height': fullheight, 'overflow':'hidden', 'padding':0 });
        $('.halffullscreen').css({'float':'left','width':($(window).width())/2, 'background-color':'#fff','margin':0, 'height': fullheight, 'overflow':'hidden', 'padding':0 });
        $('.halffullscreen img').css({'width':(($(window).width())/2), 'height': 'auto', 'margin':0, 'padding':0});
        $('.spanfullscreen img').css({'width':($(window).width()), 'height': 'auto', 'margin':0, 'padding':0});
        $('.carousel-control').show()
    }
    
    set_first_page();
    
});