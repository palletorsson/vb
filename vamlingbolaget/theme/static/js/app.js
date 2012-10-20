
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


//vyer //handelbars = ett templatesprak
CartItemView = Backbone.View.extend({
    tagName : 'li', //skapa vyn for varje rad = li-tag
    templateHtml: '<span> <%= cart %> </span>',
    
    initialize : function(){
        this.template = _.template(this.templateHtml) //_ ar underscoreklassen som man typ extendar har
        this.render()
    },
    
    render : function(){
        this.$el.html(this.template(this.model.toJSON()));
    },
    
})

CartView = Backbone.View.extend({ //el = elementet for hela vyn, $el samma wrappad i jquery, dessa skapas automatiskt och ar egenskaper till objektet
    tagName : 'div', //skapa vyn i vad yttre koden
    templateHtml: '<ul id="cartList"> </ul>', //inre koden
    
    initialize : function(){
        this.template = _.template(this.templateHtml)
        this.list = new CartItemCollection()
        var _this = this;
        this.list.bind('reset', function(){ //binder till event
            _this.onReset()  //nar listan populeras, kor onReset
        });
        this.list.fetch()
        console.log('int')
    },

    onReset: function(){
        this.render()
    },    

    render : function(){
        this.$el.html(this.template())
        _.each(this.list.models, function(elem){
            var view = new CartItemView({model:elem})
            jQuery('#cartList').append(view.$el);
        })
        this.template();
    },
    //lägger till att man kan klicka på raden och spara ner att de ar klara
    /*events: {
        'click .btn-success': 'addItem' //binder onClick till clicket 
    },*/
    
    addItem: function(){
        console.log('click')
        /*var done = this.model.get('cart');
        var label = this.model.get('label');
        this.model.set('done', !done);
        this.model.set('label','tjenis');
        this.model.save();*/
    }
})

var appView = new CartView();

jQuery('#app-canvas').append(appView.$el)

jQuery('.btn-success').click(function(){
    var cartitem = new CartItemModel();
    //cartitem.set('cart','Ny cart');
    var cartitemcoll = new CartItemCollection({model:cartitem});
    var foo = new CartItemView({model:cartitemcoll});
    console.log(foo)
    cartitem.save()
});

