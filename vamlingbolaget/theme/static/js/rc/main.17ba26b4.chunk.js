(this["webpackJsonpcod-stickeri"]=this["webpackJsonpcod-stickeri"]||[]).push([[0],{12:function(e,t,a){e.exports=a(19)},18:function(e,t,a){},19:function(e,t,a){"use strict";a.r(t);var r=a(0),i=a.n(r),l=a(5),n=a.n(l),c=a(3),o=a(6),s=a(7),m=a(10),d=a(8),u=a(2),p=a(11),g=a(9),k=a.n(g),h=function(e){var t=e.article,a=e.price,r=(e.size,e.img),l=e.sku,n=(e.id,e.chooseCod),c=e.itemid,o=e.cod_cost;return i.a.createElement("div",{className:"col-sm-4 p-3",id:c},i.a.createElement("div",{className:"card cardcontrolsmall"},i.a.createElement("a",{onClick:function(e){return n("article",l,t,r,a,c,o)}},i.a.createElement("img",{className:"card-img-top",src:"/media/"+r,alt:"Vamlingbolaget: "+t}),i.a.createElement("div",{className:"card-body"},i.a.createElement("p",{className:"card-title text-muted"}," ",t," "),i.a.createElement("p",{className:"card-text"},i.a.createElement("small",{className:"text-muted"}," ",a," SEK"))))),i.a.createElement("img",{src:"exempel-pa-plagg",alt:"exempel"}))},_=function(e){e.quality_name;var t=e.color_num,a=e.pattern_num,r=e.pattern_name,l=e.color_name,n=e.skey,c=e.itemid,o=e.makeimg,s=e.chooseCod,m=e.modaltarget,d=e.modaltarget_d;return i.a.createElement("div",{className:"col-sm-3",id:c},i.a.createElement("div",{className:"card cardcontrollarge"},i.a.createElement("a",{onClick:function(e){return s("colorsandpatterns",t,a,l,r,o,c)}},i.a.createElement("img",{className:"card-img-top",alt:"M\xf6nster "+a+" F\xe4rger "+t,src:"/media/tyger/"+t+"f_"+a+"m.jpg",width:"100%",key:n}),i.a.createElement("div",{className:"card-body"},i.a.createElement("p",{className:"card-text"},i.a.createElement("small",{className:"text-muted ml-1"},l,", ",r),i.a.createElement("span",{className:"ml-2"},i.a.createElement("button",{type:"button",className:"btn btn-light","data-toggle":"modal","data-target":d},i.a.createElement("img",{className:"icon",src:"/theme/static/svg/zoom-in.svg",alt:"zoom-in"})),i.a.createElement("div",{className:"modal fade bd-example-modal-lg",id:m,tabIndex:"-1",role:"dialog","aria-labelledby":"myLargeModalLabel","aria-hidden":"true"},i.a.createElement("div",{className:"modal-dialog modal-lg"},i.a.createElement("div",{className:"modal-content"},i.a.createElement("img",{className:"card-img-top",alt:"M\xf6nster "+a+" F\xe4rger "+t,src:"/media/tyger/"+t+"f_"+a+"m.jpg",width:"100%",id:"{i}"}))))))))))},y=function(e){var t=e.size,a=e.addSizeToArt,r=e.key,l=e.sizeid;return i.a.createElement("li",{className:"page-item sizeitem",onClick:function(){return a(t,l)},id:t,key:r},i.a.createElement("a",{className:"page-link",id:l},t))},v=function(e){e.part;return i.a.createElement("div",null,i.a.createElement("ul",{className:"btn-group mr-2 justify-content-center nav nav-tabs",role:"group","aria-label":"cod group"},i.a.createElement("li",{className:"nav-item"},i.a.createElement("a",{className:"nav-link active",id:"intro-tab","data-toggle":"tab",href:"#intro",role:"tab","aria-controls":"intro","aria-selected":"true"},i.a.createElement("span",{className:"badge badge-light"},i.a.createElement("span",null,"Cut on Demand")))),i.a.createElement("li",{className:"nav-item"},i.a.createElement("a",{className:"nav-link",id:"art-tab","data-toggle":"tab",href:"#art",role:"tab","aria-controls":"art","aria-selected":"true"},i.a.createElement("span",{className:"artorderok"},i.a.createElement("img",{className:"icon",src:"/theme/static/svg/arrow-circle-right.svg",alt:"arrow-circle-right"})),i.a.createElement("span",{className:"badge badge-light"},i.a.createElement("span",{className:"article_name",id:"article_name"},"V\xe4lj modell"),i.a.createElement("span",{className:"article_id",id:"article_id"})))),i.a.createElement("li",{className:"nav-item"},i.a.createElement("a",{className:"nav-link",id:"colorandpattern-tab","data-toggle":"tab",href:"#patterandcolor",role:"tab","aria-controls":"patterandcolor","aria-selected":"true"},i.a.createElement("span",{className:"artorderok"},i.a.createElement("img",{className:"icon",src:"/theme/static/svg/arrow-circle-right.svg",alt:"arrow-circle-right"})),i.a.createElement("span",{className:"badge badge-light"},i.a.createElement("span",{className:"pattern_name",id:"pattern_name"},"V\xe4lj Tyg"),i.a.createElement("span",{className:"pattern_id",id:"pattern_id"})))),i.a.createElement("li",{className:"nav-item"},i.a.createElement("a",{className:"nav-link",id:"order-tab","data-toggle":"tab",href:"#order",role:"tab","aria-controls":"order","aria-selected":"true"},i.a.createElement("span",{className:"pcorderok"},i.a.createElement("img",{className:"icon",src:"/theme/static/svg/arrow-circle-right.svg",alt:"arrow-circle-right"})),i.a.createElement("span",{className:"badge badge-light"},"V\xe4lj storlek")))))},f=function(){return i.a.createElement("div",{id:"intro",className:"tab-pane fadein active"},i.a.createElement("div",{className:"card mb-3"},i.a.createElement("img",{className:"card-img-top",src:"/media/cod_s.jpg",alt:"Card image cap"})))},b=function(e){var t=e.orderitem,a=e.sizes,r=e.addToShoppingCart,l=e.addSizeToArt,n=e.artok,c=e.patterncolorok,o=e.codokall,s=e.sizebase;return i.a.createElement("div",{id:"order",className:"tab-pane fadein"},i.a.createElement("div",{className:"card text-center"},i.a.createElement("div",{className:"card-header"},t.article," : ",i.a.createElement("span",{id:"the_price"}," ",t.price," ")," SEK + CUT ON DEMAND: ",i.a.createElement("span",{id:"the_cod_cost"},t.cod_cost," ")," SEK")),i.a.createElement("div",{className:"card-body row"},i.a.createElement("div",{className:"col-sm-4"},i.a.createElement("div",{className:"card"},i.a.createElement("div",{className:"card-body"},n?"":i.a.createElement("p",{className:"card-text"}," V\xe4lj modell "),i.a.createElement("p",{className:"card-text"}," ",t.article," (",i.a.createElement("span",{id:"article_sku"}," ",t.sku,")")),i.a.createElement("hr",null),i.a.createElement("p",{className:"card-img-bottom"},i.a.createElement("img",{className:"img-thumbnail",style:{width:"300px"},src:"/media/"+t.img,alt:""})," ")))),i.a.createElement("div",{className:"col-sm-4"},i.a.createElement("div",{className:"card"},i.a.createElement("div",{className:"card-body"},c?"":i.a.createElement("p",{className:"card-text"}," V\xe4lj Tyg "),i.a.createElement("p",{className:"card-text"},i.a.createElement("span",null,t.pattern_name,", ",t.color_name," ")),i.a.createElement("hr",null),i.a.createElement("p",{className:"card-img-bottom"},i.a.createElement("img",{className:"img-thumbnail",src:"/media/tyger/"+t.pcimg,alt:""})," ")))),i.a.createElement("div",{className:"col-sm-4"},i.a.createElement("div",{className:"card"},i.a.createElement("div",{className:"card-body"},i.a.createElement("p",{className:"card-title"}," V\xe4lj Storlek "),i.a.createElement("hr",null),i.a.createElement("p",{className:"card-text"},i.a.createElement("nav",null,i.a.createElement("ul",{className:"pagination"},i.a.createElement(N,{sizes:a,addSizeToArt:l,sizebase:s}))),i.a.createElement("hr",null),i.a.createElement("span",null," Sammanfatting "),i.a.createElement("hr",null),i.a.createElement("small",null,i.a.createElement("p",null,"Modell: ",t.article),i.a.createElement("p",null,"F\xe4rg: ",t.color_name),i.a.createElement("p",null,"M\xf6nster: ",t.pattern_name),i.a.createElement("p",null,"Storlek: ",t.size),i.a.createElement("p",null,"Pris: ",t.price," SEK + "),i.a.createElement("p",null,"CUT ON DEMAND: ",t.cod_cost," SEK ")),i.a.createElement("hr",null)),i.a.createElement("a",{className:"btn btn-primary",onClick:function(e){return r(t)}},i.a.createElement("span",{className:o?"showthis":"hidethis"}," L\xe4gg till i shoppingbag")))))),i.a.createElement("hr",null))},E=function(e){var t=e.arts,a=e.chooseCod;return i.a.createElement("div",{id:"art",className:"tab-pane fade scrollart"},i.a.createElement("div",{className:"row"},t.map((function(e,t){return i.a.createElement(h,Object.assign({key:t,chooseCod:a},e,{itemid:"artid_"+e.id,price:e.price,cod_cost:e.cod_cost}))}))))},S=function(e){var t=e.copa,a=e.chooseCod;return i.a.createElement("div",{id:"patterandcolor",className:"tab-pane fade scrollart"},i.a.createElement("div",{className:"row"},t.map((function(e,t){return i.a.createElement(_,Object.assign({skey:"key"+e.color_num+e.pattern_num,chooseCod:a},e,{makeimg:e.color_num+"f_"+e.pattern_num+"m.jpg",modaltarget_d:"#"+e.color_num+"f_"+e.pattern_num+"m",modaltarget:e.color_num+"f_"+e.pattern_num+"m",itemid:"id_"+e.color_num+"f_"+e.pattern_num+"m"}))}))),i.a.createElement("img",{src:"/media/exempel-pa-plagg.jpg",alt:"exempel"}))},N=function(e){var t=e.sizes,a=e.addSizeToArt,r=e.sizebase;return i.a.createElement("nav",{"aria-label":"Page navigation example"},i.a.createElement("ul",{className:"pagination"},t.map((function(e,t){return i.a.createElement(y,{key:t,size:e,sizeid:C(t,r),addSizeToArt:a})}))))};function C(e,t){var a=parseInt(e)+parseInt(t);return console.log(a,e,t),a}var j=a(1),w=a.n(j);i.a.window=window;var x=function(e){function t(e){var a,r;return Object(o.a)(this,t),(r=Object(m.a)(this,Object(d.a)(t).call(this,e))).state=(a={vPages:[{page:1}],patternsX:[],allColors:[],products:[{product:"Loading rea...",price:"... please wait",img:""}],allProducts:[],articles:[{category:"Kvinna",description:"Jacka med blixtl\xe5s mitt fram och n\xe5got insv\xe4ngd midja. Rund hals kantad med silkestrik\xe5-tyg p\xe5 insidan. ",price:1990,article:"Stickeri Jacka med blixtl\xe5s",quality:"Stickat i ekologisk ull",id:53,sku:"1221",cod_cost:100,img:"uploads/1_stickeri_jacka.jpg",pk:53,type:"Stickeri"},{category:"Kvinna",description:"A-formad kappa med blixtl\xe5s mitt fram och fickor i sids\xf6mmen. Rund halsringning kantad med silkestrik\xe5-tyg p\xe5 insidan.",price:2675,article:"Stickeri Kappa med blixtl\xe5s ",quality:"Stickat i ekologisk ull",id:54,sku:"1222",cod_cost:150,img:"uploads/1_stickeri_kappa.jpg",pk:54,type:"Stickeri"},{category:"Kvinna",description:"Tr\xf6ja med rund halsringning kantad med silkestrik\xe5-tyg p\xe5 insidan i halsen.",price:1490,article:"Stickeri Tr\xf6ja",quality:"Stickat i ekologisk ull",id:55,sku:"1320",cod_cost:100,img:"uploads/1_stickeri_troja.jpg",pk:55,type:"Stickeri"},{category:"Kvinna",description:"Enkel kort kjol med res\xe5r i midjan, kantad med silkestrik\xe5-tyg p\xe5 insidan av midjan.",price:990,article:"Stickeri Kort kjol",quality:"Stickat i ekologisk ull",id:56,sku:"1223",cod_cost:100,img:"uploads/120/1_stickeri_rak_kjol.jpg",pk:56,type:"Stickeri"},{category:"Kvinna",description:"Smal byxa med res\xe5r i midjan. Midjan \xe4r kantad med silkestrik\xe5-tyg p\xe5 insidan.",price:1370,article:"Stickeri Smala byxor",quality:"Stickat i ekologisk ull",id:57,sku:"1324",cod_cost:100,img:"uploads/120/1_smala_byxor-1.jpg",pk:57,type:"Stickeri"},{category:"Stickeri 100 % ull",description:"Raka byxor med res\xe5r i midjan, kantad med silkestrik\xe5-tyg p\xe5 insidan i midjan.",price:1370,article:"Stickeri vida byxor",quality:"Stickat i ekologisk ull",id:99,sku:"1325",cod_cost:100,img:"uploads/120/1_stickeri_raka_byxor.jpg",pk:99,type:"Stickeri"}],patternsandcolors:[{quality_num:12,color_num:168,color_name:"M\xf6rk Indigo & Vit",pattern_num:150,quality_name:"Stickat i ekologisk ull",pattern_name:"Vallmoruta"},{quality_num:12,color_num:167,color_name:"M\xf6rk indigo & Kobolt",pattern_num:200,quality_name:"Stickat i ekologisk ull",pattern_name:"Vallmoruta"},{quality_num:12,color_num:167,color_name:"M\xf6rk indigo & Kobolt",pattern_num:152,quality_name:"Stickat i ekologisk ull",pattern_name:"V\xe5gen"},{quality_num:12,color_num:166,color_name:"Vit & Ljusr\xf6d",pattern_num:150,quality_name:"Stickat i ekologisk ull",pattern_name:"Vallmoruta"},{quality_num:12,color_num:165,color_name:"M\xf6rkr\xf6d & R\xf6d",pattern_num:154,quality_name:"Stickat i ekologisk ull",pattern_name:"Stor Snedruta"},{quality_num:12,color_num:164,color_name:"Svart & Bl\xe5lila",pattern_num:151,quality_name:"Stickat i ekologisk ull",pattern_name:"Harlekin"},{quality_num:12,color_num:163,color_name:"Bl\xe5lila & Ceris",pattern_num:153,quality_name:"Stickat i ekologisk ull",pattern_name:"Sinus"},{quality_num:12,color_num:161,color_name:"Vinr\xf6d & Ceris",pattern_num:152,quality_name:"Stickat i ekologisk ull",pattern_name:"V\xe5gen"},{quality_num:12,color_num:160,color_name:"Gr\xf6n & Svart",pattern_num:151,quality_name:"Stickat i ekologisk ull",pattern_name:"Harlekin"},{quality_num:12,color_num:150,color_name:"Svart & Vit",pattern_num:153,quality_name:"Stickat i ekologisk ull",pattern_name:"Sinus"},{quality_num:12,color_num:150,color_name:"Svart & Vit",pattern_num:152,quality_name:"Stickat i ekologisk ull",pattern_name:"V\xe5gen"},{quality_num:12,color_num:150,color_name:"Svart & Vit",pattern_num:150,quality_name:"Stickat i ekologisk ull",pattern_name:"Vallmoruta"},{quality_num:12,color_num:151,color_name:"Brun & Beige",pattern_num:152,quality_name:"Stickat i ekologisk ull",pattern_name:"V\xe5gen"},{quality_num:12,color_num:7,color_name:"Svart Vit",pattern_num:151,quality_name:"Stickat i ekologisk ull",pattern_name:"Harlekin"}],sizes:["XS","S","M","L","XL","XXL"],defSizes:["S","M","L"],defPatterns:{},defColors:{},showCod:!1,showRea:!1,showCategory:!0,fullProducts:[],variations:[]},Object(c.a)(a,"sizes",[]),Object(c.a)(a,"sizebase",1),Object(c.a)(a,"singleCod",[]),Object(c.a)(a,"shopMenu",[{title:"Kvinna",Mid:"M1",type:"category"},{title:"Man",Mid:"M2",type:"category"},{title:"Barn",Mid:"M3",type:"category0"},{title:"Accessoarer & s\xe4ngkl\xe4der",Mid:"M4",type:"category0"},{title:"Metervara",Mid:"M8",type:"category0"},{title:"M\xf6nster och F\xe4rger",Mid:"M5",type:"mf"},{title:"Rea",Mid:"M6",type:"rea"},{title:"Cut on Demand",Mid:"M7",type:"cod"}]),Object(c.a)(a,"artok",!1),Object(c.a)(a,"patterncolorok",!1),Object(c.a)(a,"sizeok",!1),Object(c.a)(a,"codokall",!1),a),r.filterSearchList=r.filterSearchList.bind(Object(u.a)(r)),r.filterResetList=r.filterResetList.bind(Object(u.a)(r)),r.filterByPattern=r.filterByPattern.bind(Object(u.a)(r)),r.filterByColor=r.filterByColor.bind(Object(u.a)(r)),r.filterBySize=r.filterBySize.bind(Object(u.a)(r)),r.createPatternList=r.createPatternList.bind(Object(u.a)(r)),r.filterByPattern=r.filterByPattern.bind(Object(u.a)(r)),r.createColorList=r.createColorList.bind(Object(u.a)(r)),r.filterByPage=r.filterByPage.bind(Object(u.a)(r)),r.createPages=r.createPages.bind(Object(u.a)(r)),r.MenuClick=r.MenuClick.bind(Object(u.a)(r)),r.filterByCategory=r.filterByCategory.bind(Object(u.a)(r)),r.chooseCod=r.chooseCod.bind(Object(u.a)(r)),r.getWords=r.getWords.bind(Object(u.a)(r)),r.filterPcByQuality=r.filterPcByQuality.bind(Object(u.a)(r)),r.addToShoppingCart=r.addToShoppingCart.bind(Object(u.a)(r)),r.addSizeToArt=r.addSizeToArt.bind(Object(u.a)(r)),r.checkAllCod=r.checkAllCod.bind(Object(u.a)(r)),r}return Object(p.a)(t,e),Object(s.a)(t,[{key:"componentDidMount",value:function(){var e=function(e){var t=null;if(document.cookie&&""!==document.cookie)for(var a=document.cookie.split(";"),r=0;r<a.length;r++){var i=w.a.trim(a[r]);if(i.substring(0,e.length+1)==e+"="){t=decodeURIComponent(i.substring(e.length+1));break}}return t}("csrftoken");this.setState({csrftoken:e}),w.a.ajaxSetup({beforeSend:function(t,a){var r;r=a.type,!/^(GET|HEAD|OPTIONS|TRACE)$/.test(r)&&function(e){var t="//"+document.location.host,a=document.location.protocol+t;return e==a||e.slice(0,a.length+1)==a+"/"||e==t||e.slice(0,t.length+1)==t+"/"||!/^(\/\/|http:|https:).*/.test(e)}(a.url)&&t.setRequestHeader("X-CSRFToken",e)}})}},{key:"addToShoppingCart",value:function(e){console.dir(e,this.state.singleCod.size_id);var t={article_sku:e.sku,color:e.color_id,color2:0,pattern:e.pattern_id,pattern2:0,size:this.state.singleCod.size_id,s_type:"COD",csrfmiddlewaretoken:this.state.csrftoken,cartitem_id:"1",quantity:"1",add_or_edit:"add"};console.log(t),w.a.ajax({type:"POST",url:"/cart/addtocart/",data:t,success:function(e){e.message.msg;var t=e.cartitem;console.log(t);var a=w()("#widget_text_start").text(),r=(w()("#widget_size").text(),w()("#widget_exist").text(),w()("#widget_text_end").text(),w()("#widget_text_in").text(),w()(".size_active").text()),i=w()("#the_cod_cost").text(),l=w()("#the_price").text();if(void 0==t.color2)var n=t.color,c=t.pattern;else n=t.color+" / "+t.color2,c=t.pattern+" / "+t.pattern2;w()("#updatecart").animate({height:"200px"}),w()("#updatecart").html("<hr> <li> <strong> "+a+" </strong></li><hr><li>"+t.article+" </li><li> - "+r+" </li><li> "+n+", "+c+" </li> <div>").fadeIn(),w()("#updatecart").delay(6e3).fadeOut(3e3).animate({height:"0px"});var o=w()("#widget_quantity").text(),s=parseInt(t.quantity)+parseInt(o);w()("#widget_quantity").text(s);var m=w()("#widget_total").text(),d=parseInt(l)+parseInt(i)+parseInt(m);w()("#widget_total").text(d),w()(".button_has_item").css({borderStyle:"groove",borderWidth:"5px",borderColor:"#ff0000"})}})}},{key:"getWords",value:function(){var e=[];e.colorsandpatterns=w()("#colorsandpatterns").text(),console.log("w",e.colorsandpatterns),this.setState({words:e})}},{key:"filterPcByQuality",value:function(e){var t=e;this.state;return t=t.filter((function(e){if("Silkestrik\xe5"==e.quality_name)return e}))}},{key:"MenuClick",value:function(e,t,a,r,i,l,n){"category"==e||"category0"==e?("category"==e?this.filterByCategory(a):this.filterByCategory2(a),this.setState({showCod:!1,showRea:!1,showCategory:!0})):"rea"==e?this.setState({showCod:!1,showRea:!0,showCategory:!1}):"cod"==e?this.setState({showCod:!0,showRea:!1,showCategory:!1}):console.log("show",e)}},{key:"checkAllCod",value:function(){this.state.artok&&this.state.patterncolorok&&this.setState({codokall:!0})}},{key:"chooseCod",value:function(e){var t,a=this,r=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,i=arguments.length>2&&void 0!==arguments[2]?arguments[2]:null,l=arguments.length>3&&void 0!==arguments[3]?arguments[3]:null,n=arguments.length>4&&void 0!==arguments[4]?arguments[4]:null,c=arguments.length>5&&void 0!==arguments[5]?arguments[5]:null,o=arguments.length>6&&void 0!==arguments[6]?arguments[6]:null;(console.log(e,r,i,l,n,c,o),"article"==e)?(w()("#article_name").text(i),(t=this.state.singleCod).article=i,t.sku=r,t.img=l,t.price=n,t.cod_cost=o,w()(".bs-art-success ").remove(),w()("#"+n+" > div > a > div > p.card-title").prepend("<span class='badge bs-art-success badge-success'>+</span>"),this.checkAllCod(),k()("/products/codartjsonsingle/"+r+"/").then((function(e){return e.json()})).then((function(e){if("Barn"==e.single.category)var r=25;else r=1;a.setState({singleCod:t,artok:!0,sizes:e.sizes,sizebase:r})}))):((t=this.state.singleCod).pattern_name=l,t.pattern_id=i,t.color_name=n,t.color_id=r,t.pcimg=c,this.setState({singleCod:t,patterncolorok:!0}),this.checkAllCod(),w()("#pattern_name").text(l+", "+n),w()(".bs-pc-success").remove(),w()("#"+o+" > div > a > div > p").prepend("<span class='badge bs-pc-success badge-success'>+</span>"))}},{key:"filterResetList",value:function(e){this.setState({products:this.state.allProducts}),document.getElementById("textsearch").value=""}},{key:"addSizeToArt",value:function(e,t){console.dir(e),console.log("id: ",t);var a=this.state.singleCod;a.size=e,a.size_id=t,this.setState({singleCod:a}),w()(".sizeitem").removeClass("active"),w()("#"+e).addClass("active"),this.checkAllCod()}},{key:"filterByPattern",value:function(e,t){var a=this.state.allProducts,r=this.state;a=a.filter((function(e){return-1!==w.a.inArray(e.pattern,r.defPatterns[t].family)})),this.setState({products:a})}},{key:"filterByCategory",value:function(e){var t=this.state.fullProducts;console.log(t);this.state;t=t.filter((function(t){if(t.category==e){var a=t;return console.log(t.category,e),a}})),this.setState({fullProductsFiltered:t})}},{key:"filterByCategory2",value:function(e){console.log(e);var t=this.state.variations;this.state;t=t.filter((function(t){if(t.category==e)return console.log(t.category),t})),this.setState({fullProductsFiltered:t})}},{key:"filterBySize",value:function(e){var t=this.state.allProducts;t=t.filter((function(t){return-1!==t.size.search(e.target.id)})),this.setState({products:t})}},{key:"filterByPage",value:function(e,t){var a=this.state.allProducts,r=40*e.target.id,i=0;a=a.filter((function(e){if(i<r&&i>r-40)return e;i++})),this.setState({products:a})}},{key:"filterByColor",value:function(e,t){var a=this.state.allProducts,r=this.state;a=a.filter((function(e){return-1!==w.a.inArray(e.color,r.defColors[t].family)})),this.setState({products:a})}},{key:"createPages",value:function(e){for(var t=Math.ceil(e.length/40),a=[],r=1;r<t+1;r++)a.push({page:r});this.setState({vPages:a})}},{key:"createPatternList",value:function(e){var t=[];w.a.each(e,(function(e,a){-1===w.a.inArray(a.pattern,t)&&t.push(a.pattern)})),this.setState({patternsX:t})}},{key:"createColorList",value:function(e){var t=[];w.a.each(e,(function(e,a){-1===w.a.inArray(a.color,t)&&t.push(a.color)})),this.setState({allColors:t})}},{key:"filterSearchList",value:function(e){var t=this.state.allProducts;t=t.filter((function(t){return-1!==t.article.toLowerCase().search(e.target.value.toLowerCase())})),this.setState({products:t})}},{key:"render",value:function(){return i.a.createElement("div",{className:"container"},i.a.createElement("div",null,i.a.createElement(v,null),i.a.createElement("div",{className:"tab-content",id:"myTabContent"},i.a.createElement(f,null),i.a.createElement(E,{arts:this.state.articles,chooseCod:this.chooseCod}),i.a.createElement(S,{copa:this.state.patternsandcolors,chooseCod:this.chooseCod}),i.a.createElement(b,{orderitem:this.state.singleCod,sizes:this.state.sizes,patterncolorok:this.state.patterncolorok,artok:this.state.artok,addToShoppingCart:this.addToShoppingCart,addSizeToArt:this.addSizeToArt,codokall:this.state.codokall,sizebase:this.state.sizebase}))))}}]),t}(r.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));a(18);window.React=i.a,n.a.render(i.a.createElement(x,null),document.getElementById("react-container")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[12,1,2]]]);
//# sourceMappingURL=main.17ba26b4.chunk.js.map