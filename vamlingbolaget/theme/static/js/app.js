
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
    tagName : 'span', //skapa vyn for varje rad = li-tag
    templateHtml: '<span class="btn btn-success"> Lägg till i Köplista </span>',
    
    initialize : function(){
        this.template = _.template(this.templateHtml) //_ ar underscoreklassen som man typ extendar har
        this.render()
    },
    
    render : function(){
        this.$el.html(this.template(this.model.toJSON()));
    },
    //lägger till att man kan klicka på raden och spara ner att de ar klara
    events : {
        'click': 'onClick' //binder onClick till clicket
    
    },

    onClick : function(){
        var new_item = new MyModel();
        var sku_number = $('#sku_number').text();
        var cart = $('#sku_number').text();
        var pattern_id = $('#pattern option:selected').val();
        var color_id = +$('#color option:selected').val();
        var size_id = $('#size option:selected').val();
        var article_id = $('#article_pk').text();
        article_id = "api/v1/articles/"+article_id+"/";
        color_id  = "api/v1/colors/"+color_id+"/";
        pattern_id  = "api/v1/pattern/"+pattern_id+"/";
        size_id = "api/v1/size/"+size_id+"/";
        new_item.set({
                      'cart': cart,
                      'article.id': article_id,
                      'color': color_id,
                      'pattern': pattern_id,
                      'size': size_id,
                      'quantity': '2'
                         });

            new_item.save();
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
            jQuery('#myList').html(view.$el);
        })
        this.template();
    }
})

var appView = new MyView();

jQuery('#app-canvas').html('')
jQuery('#app-canvas').html(appView.$el)
