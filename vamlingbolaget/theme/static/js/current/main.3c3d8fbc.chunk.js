(this["webpackJsonpvb-market"]=this["webpackJsonpvb-market"]||[]).push([[0],{18:function(e,t,a){},19:function(e,t,a){"use strict";a.r(t);var s=a(3),c=a.n(s),r=a(7),i=a.n(r),n=a(8),l=a(9),o=a(2),d=a(11),j=a(10),h=a(6),b=a.n(h),m=a(4),u=a(0),p=function(e){var t=e.article,a=e.price,s=e.reaprice,c=e.pattern,r=e.color,i=(e.size,e.img),n=(e.sku,e.id);return Object(u.jsx)("div",{className:"col-sm-3  shopimgextra ",children:Object(u.jsx)("div",{className:"card cardcontrolmedium border-0",children:Object(u.jsxs)("a",{href:"/products/rea/"+n+"/",children:[Object(u.jsx)("img",{className:"card-img-top",src:"http://www.vamlingbolaget.com/media/"+i,alt:"Vamlingbolaget:"+t}),Object(u.jsxs)("div",{className:"card-body carddivextra",children:[Object(u.jsxs)("p",{className:"card-text",children:[" ",t," "]}),Object(u.jsxs)("p",{className:"card-text",children:[" ",s," SEK "]}),Object(u.jsx)("p",{className:"card-text",children:Object(u.jsxs)("small",{className:"text-muted",children:["( \u25bc ",a,")"]})}),Object(u.jsx)("p",{className:"card-text",children:Object(u.jsxs)("small",{children:[" ",c," ",r," "]})})]})]})})})},g=function(e){var t=e.category,a=e.article,s=e.img,c=e.price,r=e.pattern,i=e.color,n=(e.size,e.description,e.color_id),l=e.pattern_id,o=e.sku,d=(e.id,e.pk);return Object(u.jsx)("div",{className:"col-sm-3 shopimgextra",children:Object(u.jsx)("div",{className:"card cardcontrolmedium mb-3 border-0",children:Object(u.jsxs)("a",{href:"Barn"==t||"Accessoarer & s\xe4ngkl\xe4der"==t||"Metervara"==t?"http://www.vamlingbolaget.com//products/"+d:"http://www.vamlingbolaget.com/products/fullvariation/"+d,children:[Object(u.jsx)("img",{className:"card-img-top",src:"Barn"==t||"Accessoarer & s\xe4ngkl\xe4der"==t||"Metervara"==t?"http://www.vamlingbolaget.com/"+s:"http://www.vamlingbolaget.com/media/variations/"+o+"_"+l+"_"+n+"_1.jpg",width:"160px",alt:"Vamlingbolaget"}),Object(u.jsxs)("div",{className:"card-body carddivextra",children:[Object(u.jsxs)("p",{children:[" ",a,"  "]}),Object(u.jsxs)("p",{children:[c," SEK "]}),Object(u.jsx)("p",{children:Object(u.jsxs)("small",{children:["  ",i,"  ",r," "]})})]})]})})})},x=function(e){var t=e.products;return Object(u.jsx)("div",{children:Object(u.jsx)("div",{className:"row",children:t.map((function(e,t){return Object(u.jsx)(p,Object(m.a)({},e),t)}))})})},O=function(e){var t=e.products;return Object(u.jsx)("div",{className:"row",children:t.map((function(e,t){return Object(u.jsx)(g,Object(m.a)({},e),t)}))})},v=function(e){var t=e.pattern,a=(e.icon,e.fam,e.i,e.filterByPattern);return Object(u.jsx)("li",{className:"box page-item",id:t,onClick:function(e){return a(e,t)},children:Object(u.jsx)("a",{className:"page-link",children:Object(u.jsx)("img",{id:t,className:"iconimg",src:"/media/"+t+".png"})})})},f=function(e){var t=e.patterns,a=e.filterByPattern;return Object(u.jsx)("span",{children:Object.keys(t).map((function(e,s){return Object(u.jsx)(v,{icon:t[e].icon,pattern:e,fam:t[e].family,filterByPattern:a},s)}))})},y=function(e){var t=e.items,a=e.filterByColor;return Object(u.jsx)("span",{name:"colors",children:Object.keys(t).map((function(e,s){return Object(u.jsx)("li",{className:"page-item box",id:t[e].color,onClick:function(s){return a(s,t[e].color)},children:Object(u.jsx)("a",{className:"page-link",id:s,children:Object(u.jsx)("div",{style:t[e].colorvalue,className:"boxline"})})},s)}))})},N=function(e){var t=e.size,a=e.i;return Object(u.jsxs)("li",{className:"box page-item",children:[" ",Object(u.jsx)("span",{className:"sizes",id:t,children:Object(u.jsx)("a",{className:"page-link",id:t,children:t})})]},a)},k=function(e){var t=e.sizes,a=e.filterBySize;return Object(u.jsx)("span",{onClick:a,children:t.map((function(e,t){return Object(u.jsx)(N,{size:e},t)}))})},C=function(e){var t=e.article,a=e.price,s=(e.size,e.img),c=e.sku,r=(e.id,e.chooseCod),i=e.itemid,n=e.cod_cost;return Object(u.jsx)("div",{className:"col-sm",id:i,children:Object(u.jsx)("div",{className:"card cardcontrolsmall",children:Object(u.jsxs)("a",{onClick:function(e){return r("article",c,t,s,a,i,n)},children:[Object(u.jsx)("img",{className:"card-img-top",src:"http://www.vamlingbolaget.com/"+s,alt:"Vamlingbolaget: "+t}),Object(u.jsxs)("div",{className:"card-body",children:[Object(u.jsxs)("p",{className:"card-title text-muted",children:[" ",t," "]}),Object(u.jsx)("p",{className:"card-text",children:Object(u.jsxs)("small",{className:"text-muted",children:[" ",a," SEK"]})})]})]})})})},_=function(e){e.quality_name;var t=e.color_num,a=e.pattern_num,s=e.pattern_name,c=e.color_name,r=e.key,i=e.itemid,n=e.makeimg,l=e.chooseCod,o=e.modaltarget,d=e.modaltarget_d;return Object(u.jsx)("div",{className:"col-sm",id:i,children:Object(u.jsx)("div",{className:"card cardcontrollarge",children:Object(u.jsxs)("a",{onClick:function(e){return l("colorsandpatterns",t,a,c,s,n,i)},children:[Object(u.jsx)("img",{className:"card-img-top",alt:"M\xf6nster "+a+" F\xe4rger "+t,src:"/media/tyger/"+t+"f_"+a+"m.jpg",width:"100%"},r),Object(u.jsx)("div",{className:"card-body",children:Object(u.jsxs)("p",{className:"card-text",children:[Object(u.jsxs)("small",{className:"text-muted ml-1",children:[c,", ",s]}),Object(u.jsxs)("span",{className:"ml-2",children:[Object(u.jsx)("button",{type:"button",className:"btn btn-light","data-toggle":"modal","data-target":d,children:Object(u.jsx)("img",{className:"icon",src:"/theme/static/svg/zoom-in.svg",alt:"zoom-in"})}),Object(u.jsx)("div",{className:"modal fade bd-example-modal-lg",id:o,tabIndex:"-1",role:"dialog","aria-labelledby":"myLargeModalLabel","aria-hidden":"true",children:Object(u.jsx)("div",{className:"modal-dialog modal-lg",children:Object(u.jsx)("div",{className:"modal-content",children:Object(u.jsx)("img",{className:"card-img-top",alt:"M\xf6nster "+a+" F\xe4rger "+t,src:"/media/tyger/"+t+"f_"+a+"m.jpg",width:"100%",id:"{i}"},r)})})})]})]})})]})})})},w=function(e){var t=e.size,a=e.addSizeToArt,s=e.key,c=e.sizeid;return Object(u.jsx)("li",{className:"page-item sizeitem",onClick:function(){return a(t,c)},id:t,children:Object(u.jsx)("a",{className:"page-link",id:c,children:t})},s)},S=function(e){e.part;return Object(u.jsx)("div",{children:Object(u.jsxs)("ul",{className:"btn-group mr-2 justify-content-center nav nav-tabs",role:"group","aria-label":"cod group",children:[Object(u.jsx)("li",{className:"nav-item",children:Object(u.jsx)("a",{className:"nav-link active",id:"intro-tab","data-toggle":"tab",href:"#intro",role:"tab","aria-controls":"intro","aria-selected":"true",children:Object(u.jsx)("span",{className:"badge badge-light",children:Object(u.jsx)("span",{children:"Cut on Demand"})})})}),Object(u.jsx)("li",{className:"nav-item",children:Object(u.jsxs)("a",{className:"nav-link",id:"art-tab","data-toggle":"tab",href:"#art",role:"tab","aria-controls":"art","aria-selected":"true",children:[Object(u.jsx)("span",{className:"artorderok",children:Object(u.jsx)("img",{className:"icon",src:"/theme/static/svg/arrow-circle-right.svg",alt:"arrow-circle-right"})}),Object(u.jsxs)("span",{className:"badge badge-light",children:[Object(u.jsx)("span",{className:"article_name",id:"article_name",children:"V\xe4lj modell"}),Object(u.jsx)("span",{className:"article_id",id:"article_id"})]})]})}),Object(u.jsx)("li",{className:"nav-item",children:Object(u.jsxs)("a",{className:"nav-link",id:"colorandpattern-tab","data-toggle":"tab",href:"#patterandcolor",role:"tab","aria-controls":"patterandcolor","aria-selected":"true",children:[Object(u.jsx)("span",{className:"artorderok",children:Object(u.jsx)("img",{className:"icon",src:"/theme/static/svg/arrow-circle-right.svg",alt:"arrow-circle-right"})}),Object(u.jsxs)("span",{className:"badge badge-light",children:[Object(u.jsx)("span",{className:"pattern_name",id:"pattern_name",children:"V\xe4lj Tyg"}),Object(u.jsx)("span",{className:"pattern_id",id:"pattern_id"})]})]})}),Object(u.jsx)("li",{className:"nav-item",children:Object(u.jsxs)("a",{className:"nav-link",id:"order-tab","data-toggle":"tab",href:"#order",role:"tab","aria-controls":"order","aria-selected":"true",children:[Object(u.jsx)("span",{className:"pcorderok",children:Object(u.jsx)("img",{className:"icon",src:"/theme/static/svg/arrow-circle-right.svg",alt:"arrow-circle-right"})}),Object(u.jsx)("span",{className:"badge badge-light",children:"V\xe4lj storlek"})]})})]})})},z=function(){return Object(u.jsx)("div",{id:"intro",className:"tab-pane fadein active",children:Object(u.jsx)("div",{className:"card mb-3",children:Object(u.jsx)("img",{className:"card-img-top",src:"/media/codtopfull.jpg",alt:"Card image cap"})})})},P=function(e){var t=e.orderitem,a=e.sizes,s=e.addToShoppingCart,c=e.addSizeToArt,r=e.artok,i=e.patterncolorok,n=e.codokall,l=e.sizebase;return Object(u.jsxs)("div",{id:"order",className:"tab-pane fadein",children:[Object(u.jsx)("div",{className:"card text-center",children:Object(u.jsxs)("div",{className:"card-header",children:[t.article," : ",Object(u.jsxs)("span",{id:"the_price",children:[" ",t.price," "]})," SEK + CUT ON DEMAND: ",Object(u.jsxs)("span",{id:"the_cod_cost",children:[t.cod_cost," "]})," SEK"]})}),Object(u.jsxs)("div",{className:"card-body row",children:[Object(u.jsx)("div",{className:"col-sm-4",children:Object(u.jsx)("div",{className:"card",children:Object(u.jsxs)("div",{className:"card-body",children:[r?"":Object(u.jsx)("p",{className:"card-text",children:" V\xe4lj modell "}),Object(u.jsxs)("p",{className:"card-text",children:[" ",t.article," (",Object(u.jsxs)("span",{id:"article_sku",children:[" ",t.sku,")"]})]}),Object(u.jsx)("hr",{}),Object(u.jsxs)("p",{className:"card-img-bottom",children:[Object(u.jsx)("img",{className:"img-thumbnail",style:{width:"300px"},src:"http://www.vamlingbolaget.com/"+t.img,alt:""})," "]})]})})}),Object(u.jsx)("div",{className:"col-sm-4",children:Object(u.jsx)("div",{className:"card",children:Object(u.jsxs)("div",{className:"card-body",children:[i?"":Object(u.jsx)("p",{className:"card-text",children:" V\xe4lj Tyg "}),Object(u.jsx)("p",{className:"card-text",children:Object(u.jsxs)("span",{children:[t.pattern_name,", ",t.color_name," "]})}),Object(u.jsx)("hr",{}),Object(u.jsxs)("p",{className:"card-img-bottom",children:[Object(u.jsx)("img",{className:"img-thumbnail",src:"/media/tyger/"+t.pcimg,alt:""})," "]})]})})}),Object(u.jsx)("div",{className:"col-sm-4",children:Object(u.jsx)("div",{className:"card",children:Object(u.jsxs)("div",{className:"card-body",children:[Object(u.jsx)("p",{className:"card-title",children:" V\xe4lj Storlek "}),Object(u.jsx)("hr",{}),Object(u.jsxs)("p",{className:"card-text",children:[Object(u.jsx)("nav",{children:Object(u.jsx)("ul",{className:"pagination",children:Object(u.jsx)(A,{sizes:a,addSizeToArt:c,sizebase:l})})}),Object(u.jsx)("hr",{}),Object(u.jsx)("span",{children:" Sammanfatting "}),Object(u.jsx)("hr",{}),Object(u.jsxs)("small",{children:[Object(u.jsxs)("p",{children:["Modell: ",t.article]}),Object(u.jsxs)("p",{children:["F\xe4rg: ",t.color_name]}),Object(u.jsxs)("p",{children:["M\xf6nster: ",t.pattern_name]}),Object(u.jsxs)("p",{children:["Storlek: ",t.size]}),Object(u.jsxs)("p",{children:["Pris: ",t.price," SEK + "]}),Object(u.jsxs)("p",{children:["CUT ON DEMAND: ",t.cod_cost," SEK "]})]}),Object(u.jsx)("hr",{})]}),Object(u.jsx)("a",{className:"btn btn-primary",onClick:function(e){return s(t)},children:Object(u.jsx)("span",{className:n?"showthis":"hidethis",children:" L\xe4gg till i shoppingbag"})})]})})})]}),Object(u.jsx)("hr",{})]})},M=function(e){var t=e.arts,a=e.chooseCod;return Object(u.jsx)("div",{id:"art",className:"tab-pane fade scrollart",children:Object(u.jsx)("div",{className:"row",children:t.map((function(e,t){return Object(u.jsx)(C,Object(m.a)(Object(m.a)({chooseCod:a},e),{},{itemid:"artid_"+e.id,price:e.price,cod_cost:e.cod_cost}),t)}))})})},B=function(e){var t=e.copa,a=e.chooseCod;return Object(u.jsx)("div",{id:"patterandcolor",className:"tab-pane fade scrollart",children:Object(u.jsx)("div",{className:"row",children:t.map((function(e,t){return Object(u.jsx)(_,Object(m.a)(Object(m.a)({chooseCod:a},e),{},{makeimg:e.color_num+"f_"+e.pattern_num+"m.jpg",modaltarget_d:"#"+e.color_num+"f_"+e.pattern_num+"m",modaltarget:e.color_num+"f_"+e.pattern_num+"m",itemid:"id_"+e.color_num+"f_"+e.pattern_num+"m"}),t)}))})})},A=function(e){var t=e.sizes,a=e.addSizeToArt,s=e.sizebase;return Object(u.jsx)("nav",{"aria-label":"Page navigation example",children:Object(u.jsx)("ul",{className:"pagination",children:t.map((function(e,t){return Object(u.jsx)(w,{size:e,sizeid:T(t,s),addSizeToArt:a},t)}))})})};function T(e,t){var a=parseInt(e)+parseInt(t);return console.log(a,e,t),a}var L=function(e){var t=e.items,a=e.MenuClick;return Object(u.jsxs)("nav",{className:"navbar navbar-expand-md bg-faded extramenu",children:[Object(u.jsx)("button",{className:"navbar-toggler",type:"button","data-toggle":"collapse","data-target":"#navbarSupportedShop","aria-controls":"navbarSupportedContent","aria-expanded":"false","aria-label":"Toggle navigation",children:Object(u.jsx)("span",{className:"navbar-toggler-icon"})}),Object(u.jsx)("ul",{className:"collapse pagination",id:"navbarSupportedShop",children:t.map((function(e){return Object(u.jsx)("li",{className:"nav-item",children:Object(u.jsxs)("span",{className:"badge badge-light nav-link a_headernav",id:e.Mid,onClick:function(){return a(e.type,e.Mid,e.title,"shopmenu")},children:[e.title," |\xa0"]})},e.Mid)}))})]})},E=a(1),I=a.n(E);c.a.window=window;var R=function(e){Object(d.a)(a,e);var t=Object(j.a)(a);function a(e){var s;return Object(n.a)(this,a),(s=t.call(this,e)).state={vPages:[{page:1}],patternsX:[],allColors:[],products:[{product:"Loading rea...",price:"... please wait",img:""}],allProducts:[],defSizes:["S","M","L"],defPatterns:{},defColors:{},showCod:!1,showRea:!0,showCategory:!0,fullProducts:[],variations:[{}],fullProductsFiltered:[],articles:[{}],patternsandcolors:[{}],sizes:[],sizebase:1,singleCod:[],shopMenu:[{title:"Kvinna",Mid:"M1",type:"category"},{title:"Man",Mid:"M2",type:"category"},{title:"Barn",Mid:"M3",type:"category0"},{title:"Accessoarer & s\xe4ngkl\xe4der",Mid:"M4",type:"category0"},{title:"Metervara",Mid:"M8",type:"category0"},{title:"M\xf6nster och F\xe4rger",Mid:"M5",type:"mf"},{title:"Rea",Mid:"M6",type:"rea"},{title:"Cut on Demand",Mid:"M7",type:"cod"}],artok:!1,patterncolorok:!1,sizeok:!1,codokall:!1},s.filterSearchList=s.filterSearchList.bind(Object(o.a)(s)),s.filterResetList=s.filterResetList.bind(Object(o.a)(s)),s.filterByPattern=s.filterByPattern.bind(Object(o.a)(s)),s.filterByColor=s.filterByColor.bind(Object(o.a)(s)),s.filterBySize=s.filterBySize.bind(Object(o.a)(s)),s.createPatternList=s.createPatternList.bind(Object(o.a)(s)),s.filterByPattern=s.filterByPattern.bind(Object(o.a)(s)),s.createColorList=s.createColorList.bind(Object(o.a)(s)),s.filterByPage=s.filterByPage.bind(Object(o.a)(s)),s.createPages=s.createPages.bind(Object(o.a)(s)),s.MenuClick=s.MenuClick.bind(Object(o.a)(s)),s.filterByCategory=s.filterByCategory.bind(Object(o.a)(s)),s.chooseCod=s.chooseCod.bind(Object(o.a)(s)),s.getWords=s.getWords.bind(Object(o.a)(s)),s.filterPcByQuality=s.filterPcByQuality.bind(Object(o.a)(s)),s.addToShoppingCart=s.addToShoppingCart.bind(Object(o.a)(s)),s.addSizeToArt=s.addSizeToArt.bind(Object(o.a)(s)),s.checkAllCod=s.checkAllCod.bind(Object(o.a)(s)),s}return Object(l.a)(a,[{key:"componentDidMount",value:function(){var e=this;b()("/products/reajson/").then((function(e){return e.json()})).then((function(t){console.log(t);var a=t;e.setState({products:a,allProducts:a}),e.createPatternList(a),e.createColorList(a),e.createPages(a)}));var t=function(e){var t=null;if(document.cookie&&""!==document.cookie)for(var a=document.cookie.split(";"),s=0;s<a.length;s++){var c=I.a.trim(a[s]);if(c.substring(0,e.length+1)==e+"="){t=decodeURIComponent(c.substring(e.length+1));break}}return t}("csrftoken");this.setState({csrftoken:t}),I.a.ajaxSetup({beforeSend:function(e,a){var s;s=a.type,!/^(GET|HEAD|OPTIONS|TRACE)$/.test(s)&&function(e){var t="//"+document.location.host,a=document.location.protocol+t;return e==a||e.slice(0,a.length+1)==a+"/"||e==t||e.slice(0,t.length+1)==t+"/"||!/^(\/\/|http:|https:).*/.test(e)}(a.url)&&e.setRequestHeader("X-CSRFToken",t)}})}},{key:"addToShoppingCart",value:function(e){console.dir(e,this.state.singleCod.size_id);var t={article_sku:e.sku,color:e.color_id,color2:0,pattern:e.pattern_id,pattern2:0,size:this.state.singleCod.size_id,s_type:"COD",csrfmiddlewaretoken:this.state.csrftoken,cartitem_id:"1",quantity:"1",add_or_edit:"add"};console.log(t),I.a.ajax({type:"POST",url:"/cart/addtocart/",data:t,success:function(e){e.message.msg;var t=e.cartitem;console.log(t);var a=I()("#widget_text_start").text(),s=(I()("#widget_size").text(),I()("#widget_exist").text(),I()("#widget_text_end").text(),I()("#widget_text_in").text(),I()(".size_active").text()),c=I()("#the_cod_cost").text(),r=I()("#the_price").text();if(void 0==t.color2)var i=t.color,n=t.pattern;else i=t.color+" / "+t.color2,n=t.pattern+" / "+t.pattern2;I()("#updatecart").animate({height:"200px"}),I()("#updatecart").html("<hr> <li> <strong> "+a+" </strong></li><hr><li>"+t.article+" </li><li> - "+s+" </li><li> "+i+", "+n+" </li> <div>").fadeIn(),I()("#updatecart").delay(6e3).fadeOut(3e3).animate({height:"0px"});var l=I()("#widget_quantity").text(),o=parseInt(t.quantity)+parseInt(l);I()("#widget_quantity").text(o);var d=I()("#widget_total").text(),j=parseInt(r)+parseInt(c)+parseInt(d);I()("#widget_total").text(j),I()(".button_has_item").css({borderStyle:"groove",borderWidth:"5px",borderColor:"#ff0000"})}})}},{key:"getWords",value:function(){var e=[];e.colorsandpatterns=I()("#colorsandpatterns").text(),console.log("w",e.colorsandpatterns),this.setState({words:e})}},{key:"filterPcByQuality",value:function(e){var t=e;this.state;return t=t.filter((function(e){if("Silkestrik\xe5"==e.quality_name)return e}))}},{key:"MenuClick",value:function(e,t,a,s,c,r,i){"category"==e||"category0"==e?("category"==e?this.filterByCategory(a):this.filterByCategory2(a),this.setState({showCod:!1,showRea:!1,showCategory:!0})):"rea"==e?this.setState({showCod:!1,showRea:!0,showCategory:!1}):"cod"==e?this.setState({showCod:!0,showRea:!1,showCategory:!1}):console.log("show",e)}},{key:"checkAllCod",value:function(){this.state.artok&&this.state.patterncolorok&&this.setState({codokall:!0})}},{key:"chooseCod",value:function(e){var t,a=this,s=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,c=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:null,i=arguments.length>4&&void 0!==arguments[4]?arguments[4]:null,n=arguments.length>5&&void 0!==arguments[5]?arguments[5]:null,l=arguments.length>6&&void 0!==arguments[6]?arguments[6]:null;(console.log(e,s,c,r,i,n,l),"article"==e)?(I()("#article_name").text(c),(t=this.state.singleCod).article=c,t.sku=s,t.img=r,t.price=i,t.cod_cost=l,I()(".bs-art-success ").remove(),I()("#"+i+" > div > a > div > p.card-title").prepend("<span class='badge bs-art-success badge-success'>+</span>"),this.checkAllCod(),b()("/products/codartjsonsingle/"+s+"/").then((function(e){return e.json()})).then((function(e){if("Barn"==e.single.category)var s=25;else s=1;a.setState({singleCod:t,artok:!0,sizes:e.sizes,sizebase:s})}))):((t=this.state.singleCod).pattern_name=r,t.pattern_id=c,t.color_name=i,t.color_id=s,t.pcimg=n,this.setState({singleCod:t,patterncolorok:!0}),this.checkAllCod(),I()("#pattern_name").text(r+", "+i),I()(".bs-pc-success").remove(),I()("#"+l+" > div > a > div > p").prepend("<span class='badge bs-pc-success badge-success'>+</span>"))}},{key:"filterResetList",value:function(e){this.setState({products:this.state.allProducts}),document.getElementById("textsearch").value=""}},{key:"addSizeToArt",value:function(e,t){console.dir(e),console.log("id: ",t);var a=this.state.singleCod;a.size=e,a.size_id=t,this.setState({singleCod:a}),I()(".sizeitem").removeClass("active"),I()("#"+e).addClass("active"),this.checkAllCod()}},{key:"filterByPattern",value:function(e,t){var a=this.state.allProducts,s=this.state;a=a.filter((function(e){return-1!==I.a.inArray(e.pattern,s.defPatterns[t].family)})),this.setState({products:a})}},{key:"filterByCategory",value:function(e){var t=this.state.fullProducts;console.log(t);this.state;t=t.filter((function(t){if(t.category==e){var a=t;return console.log(t.category,e),a}})),this.setState({fullProductsFiltered:t})}},{key:"filterByCategory2",value:function(e){console.log(e);var t=this.state.variations;this.state;t=t.filter((function(t){if(t.category==e)return console.log(t.category),t})),this.setState({fullProductsFiltered:t})}},{key:"filterBySize",value:function(e){var t=this.state.allProducts;t=t.filter((function(t){return-1!==t.size.search(e.target.id)})),this.setState({products:t})}},{key:"filterByPage",value:function(e,t){var a=this.state.allProducts,s=40*e.target.id,c=0;a=a.filter((function(e){if(c<s&&c>s-40)return e;c++})),this.setState({products:a})}},{key:"filterByColor",value:function(e,t){var a=this.state.allProducts,s=this.state;a=a.filter((function(e){return-1!==I.a.inArray(e.color,s.defColors[t].family)})),this.setState({products:a})}},{key:"createPages",value:function(e){for(var t=Math.ceil(e.length/40),a=[],s=1;s<t+1;s++)a.push({page:s});this.setState({vPages:a})}},{key:"createPatternList",value:function(e){var t=[];I.a.each(e,(function(e,a){-1===I.a.inArray(a.pattern,t)&&t.push(a.pattern)})),this.setState({patternsX:t})}},{key:"createColorList",value:function(e){var t=[];I.a.each(e,(function(e,a){-1===I.a.inArray(a.color,t)&&t.push(a.color)})),this.setState({allColors:t})}},{key:"filterSearchList",value:function(e){var t=this.state.allProducts;t=t.filter((function(t){return-1!==t.article.toLowerCase().search(e.target.value.toLowerCase())})),this.setState({products:t})}},{key:"render",value:function(){return Object(u.jsxs)("div",{className:"container",children:[Object(u.jsx)(L,{items:this.state.shopMenu,MenuClick:this.MenuClick}),Object(u.jsx)("hr",{}),this.state.showCod&&Object(u.jsxs)("div",{children:[Object(u.jsx)(S,{}),Object(u.jsxs)("div",{className:"tab-content",id:"myTabContent",children:[Object(u.jsx)(z,{}),Object(u.jsx)(M,{arts:this.state.articles,chooseCod:this.chooseCod}),Object(u.jsx)(B,{copa:this.state.patternsandcolors,chooseCod:this.chooseCod}),Object(u.jsx)(P,{orderitem:this.state.singleCod,sizes:this.state.sizes,patterncolorok:this.state.patterncolorok,artok:this.state.artok,addToShoppingCart:this.addToShoppingCart,addSizeToArt:this.addSizeToArt,codokall:this.state.codokall,sizebase:this.state.sizebase})]})]}),Object(u.jsxs)("div",{children:[Object(u.jsx)("nav",{"aria-label":"navigation",children:Object(u.jsxs)("ul",{className:"pagination pagination-sm",children:[Object(u.jsx)(y,{items:this.state.defColors,filterByColor:this.filterByColor}),Object(u.jsx)("div",{className:"menupadding",children:" "}),Object(u.jsx)(f,{patterns:this.state.defPatterns,filterByPattern:this.filterByPattern}),Object(u.jsx)("div",{className:"menupadding",children:" "}),Object(u.jsx)(k,{sizes:this.state.defSizes,filterBySize:this.filterBySize}),Object(u.jsx)("div",{className:"menupadding",children:" "}),Object(u.jsx)("input",{type:"text",placeholder:"Filter by article name",id:"textsearch",onChange:this.filterSearchList})]})}),Object(u.jsx)("hr",{}),Object(u.jsx)(x,{products:this.state.products})]}),this.state.showCategory&&Object(u.jsx)("div",{children:Object(u.jsx)(O,{products:this.state.fullProductsFiltered})})]})}}]),a}(s.Component);a(18);window.React=c.a,i.a.render(Object(u.jsx)(R,{}),document.getElementById("react-container"))}},[[19,1,2]]]);
//# sourceMappingURL=main.3c3d8fbc.chunk.js.map