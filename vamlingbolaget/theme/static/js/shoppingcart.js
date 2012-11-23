
(function($) {
var id = 1;

YourCartModel = Backbone.Tastypie.Model.extend({
    urlRoot: '/api/v1/cartitem/',
    defaults: {
    }
});

YourCartCollection = Backbone.Tastypie.Collection.extend({
    //urlRoot: '/api/v1/cartitem/' + id +'/',
    urlRoot: '/api/v1/cartitem/',

    model: YourCartModel
    //cart_id:
});

YourCartItemView = Backbone.View.extend({
    tagName : 'tr',
    templateHtml:
                    '<td width="10%"> <a href="<%= id %>"> <%= id %></a> </td>' +
                    '<td width="5%"> <i id="<%= id %>" class="icon-remove-sign"></i> </td>' +
                    '<td width="30%"> <%= article.name %> </td>' +
                    '<td width="10%"> <%= color.name %> </td>'+
                    '<td width="15%"> <%= pattern.name %> </td>'+
                    '<td width="15%"> <%= size.name %> </td>'+
                    '<td width="15%"> <%= article.price %> </td>',

    events: {
        "click i": "remove_item",
        "focus a": "update_amount"

    },

    remove_item: function(e){
        e.preventDefault();
        var id = this.model.get("id");
        console.log(this.model);
        if(confirm('Vill du ta bort denna post?')){
            this.model.destroy({
                success: function(model, response){
                    // this.remove;
                    // this.render;
                    $('#'+id).parent().parent().remove();
                    // recount the value
                },
                error: function(model, response){
                }
            });
        }

    },

    update_amount: function(e){
        e.preventDefault();
        this.set("quantity", 2);
        this.save();
    },



    initialize : function(){
        this.template = _.template(this.templateHtml)
        // this.model.bind('update_amount', this.render, this);
        // this.model.bind('remove_item', this.remove, this);
        this.render();
    },

    render : function(){
        this.$el.html(this.template(this.model.toJSON()));
        this.model.bind('change', this.render);
    }
})


YourCartView = Backbone.View.extend({
    tagName : 'span',
    templateHtml:   '',

    initialize : function(){
        _.bindAll(this, ["render"])
        this.template = _.template(this.templateHtml)
        this.list = new YourCartCollection({});
        var _this = this;
         this.list.bind('reset', function(){
            _this.onReset()
        });
        this.list.fetch()
    },

    onReset: function(){
        this.render();
    },


    render : function(){
        this.$el.html(this.template())
        _.each(this.list.models, function(elem){
            var view = new YourCartItemView({
                model:elem

            })
            $('#shoppinglist').append(view.$el);
        })
        this.template();
        return this;
    }
})

var appView = new YourCartView();

$('#shoppinglist').html(appView.$el);

})(jQuery);
