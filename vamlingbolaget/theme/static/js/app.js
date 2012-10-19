
//en instans
MyModel = Backbone.Tastypie.Model.extend({
    urlRoot: '/api/dev/my/',
    defaults: {
        'label': 'no name yet'
    }
});

//lista av instanser
MyCollection = Backbone.Tastypie.Collection.extend({
    urlRoot: '/api/dev/my/',
    model: MyModel
})


//vyer //handelbars = ett templatesprak
MyItemView = Backbone.View.extend({
    tagName : 'li', //skapa vyn for varje rad = li-tag
    templateHtml: '<span> <%= label %> </span>',
    
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
        alert('Clicked!')
        var done = this.model.get('done');
        var label = this.model.get('label');
        this.model.set('done', !done);
        this.model.set('label','tjenis');
        this.model.save();
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

var appView = new MyView();

jQuery('#app-canvas').html(appView.$el)
