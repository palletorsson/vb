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

$(function(){
    $("#color").val("{{ product.combo.color }}").attr("selected", "selected");
    $("#pattern").val("{{ product.combo.pattern }}").attr("selected", "selected");
    $("#size").val("Medium").attr("selected", "selected");

    $('#color').change(function(e){
        //e.stopPropagation();
        console.log($('select options:selected').text());
    });
    
});