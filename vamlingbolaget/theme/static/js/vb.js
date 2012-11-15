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
    var getsrc = function(me, from, to){
        var oldsrc = me.attr('src'),
            newsrc = oldsrc.replace(from,to);
        return newsrc;
    }    

    var initgallery = function(){
        $('.enlarge').hover(function(){
             $(this).attr('src', getsrc($(this), 'thumbnail','small'))
        }, function(){
             $(this).attr('src', getsrc($(this), 'small', 'thumbnail'))
        });
    
        $('.isfeatured').hover(function(){
             $(this).attr('src', getsrc($(this), 'medium','large'))
        }, function(){
             $(this).attr('src', getsrc($(this), 'large','thumbnail'))
             $(this).removeClass('isfeatured').addClass('enlarge');
             initgallery();
        }); 
    }
    initgallery();

    $('.overlay').each(function(){
        console.log($(this));
        var me = $(this);
        $(this).siblings().load(function(){
            var width = $(this).css('width'),
                pos = $(this).offset();
                
            me.css({'width': width, 'left':pos.left, 'top':pos.top, 'height': '20px', 'background-color':'#000', 'color':'#fff'});
            console.log($(this).css('width'));
        })
        
    });
    
});