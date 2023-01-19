odoo.define('website_mega_menus.editor.snippets.options', function (require) {
'use strict';

  var editor = require('web_editor.editor');
  editor.Class.include({
    save: function (reload){
      $(".mega_menu_nav button").remove();
      $('.owl-item.cloned').remove();

      // $("#customNav2 button").remove();
      // $("#best_selling_nav button").remove();
      // $("#latest_products_nav button").remove();

      $(".owl-nav button").remove();
      return this._super(reload);
    },
  });

})
