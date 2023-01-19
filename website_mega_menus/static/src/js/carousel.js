odoo.define('website_mega_menus.carousel', function(require){
  'use strict';

  var publicWidget = require("web.public.widget");

  // publicWidget.registry.CategoryCarousel = publicWidget.Widget.extend({
  //   selector: '.owl-mega_menu',
  //
  //   start: function(){
  //     this.$target.owlCarousel({
  //       items : 4,
  //       itemsDesktop : [1199,2],
  //       itemsDesktopSmall : [979,1],
  //       loop: true,
  //       dots: false,
  //       nav: true,
  //       navContainer: this.$target.closest(".mega_menu_snippet_3").find(".mega_menu_nav"),
  //     });
  //   }
  // });

  publicWidget.registry.Snippet2Carousel = publicWidget.Widget.extend({
    selector: '.mega_menu_snippet_2 .owl-mega_menu',

    start: function(){
      this.$target.on({
        'initialized.owl.carousel': function () {
           $(this).show();
        }
      }).owlCarousel({
        // items : 2,
        // itemsDesktop : [1199,2],
        // itemsDesktopSmall : [979,1],
        loop: true,
        dots: true,
        nav: true,
        margin: 10,
        navContainer: this.$target.closest(".mega_menu_snippet_2").find(".mega_menu_nav"),
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:1,
                nav:false
            },
            1000:{
                items:2,
                nav:true,
                // loop:false
            }
        }
      });
    }
  });

  publicWidget.registry.Snippet5Carousel = publicWidget.Widget.extend({
    selector: '.mega_menu_snippet_5 .owl-mega_menu',

    start: function(){
      this.$target.on({
        'initialized.owl.carousel': function () {
           $(this).show();
        }
      }).owlCarousel({
        // items : 2,
        // itemsDesktop : [1199,2],
        // itemsDesktopSmall : [979,1],
        loop: true,
        dots: false,
        nav: true,
        margin: 10,
        navContainer: this.$target.closest(".mega_menu_snippet_5").find(".mega_menu_nav"),
        responsiveClass:true,
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:1,
                nav:false
            },
            1000:{
                items:3,
                nav:true,
                // loop:false
            }
        }
      });
    }
  });
})
