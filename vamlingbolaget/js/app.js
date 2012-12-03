
//en instans
MyModel = Backbone.Tastypie.Model.extend({
    urlRoot: '/api/v1/cartitem/',
    defaults: {
        'cart': 'no cart yet'

    }
});

//lista av instanser
MyCollection = Backbone.Tastypie.Collection.extend({
    urlRoot: '/api/v1/cartitem/',
    model: MyModel
})


//vyer //handelbars = ett templatesprak
MyItemView = Backbone.View.extend({
    tagName : 'li', //skapa vyn for varje rad = li-tag
    templateHtml: '<span class="btn btn-success"> Lägg till i Köplista </span>',
    
    initialize : function(){
        this.template = _.template(this.templateHtml) //_ ar underscoreklassen som man typ extendar har
        this.render()
    },
    
    render : function(){
        this.$el.html(this.template(this.model.toJSON())); // load the
    },

    events : {
        'click': 'onClick'
    },


    onClick : function(){
        console.log("clicked");
    }

    })
    

MyView = Backbone.View.extend({ //el = elementet for hela vyn, $el samma wrappad i jquery, dessa skapas automatiskt och ar egenskaper till objektet
    tagName : 'div', //skapa vyn i vad yttre koden
    templateHtml: '<ul id="myList"> </ul>', //inre koden
    
    initialize : function(){
        this.template = _.template(this.templateHtml)
        this.list = new MyCollection()
        var _this = this;
        this.list.bind('reset', function(){ //binder till event
            _this.onReset()  //nar listan populeras, kor onReset
        });
        this.list.fetch()
    },

    onReset: function(){
        this.render()
    },    

    render : function(){
        this.$el.html(this.template())
        _.each(this.list.models, function(elem){
            var view = new MyItemView({model:elem})
            jQuery('#myList').append(view.$el);
        })
        this.template();
    }
})

// you can do getter and setters
var appView = new MyView({
cart: 1,
article: 1,
color:  1,
pattern: 1,
size: 1,
date_added: 1,
quantity: 1
});
var person = new Person({ name: "Thomas", age: 67, child: 'Ryan'});

cart = models.ForeignKey(Cart)

jQuery('#app-canvas').html('')
jQuery('#app-canvas').html(appView.$el)
